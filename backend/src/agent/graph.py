import os
import re
import time
import asyncio
import requests
from typing import List
from sqlalchemy import text

import fitz  # PyMuPDF
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.runnables import RunnableConfig
from litellm import completion
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from agent.tools_and_schemas import (
    SearchQueryList,
    Reflection,
    arxiv_tool,
    unpaywall_tool,
    zotero_tool,
)
from agent.prompts import (
    get_current_date,
    query_writer_instructions,
    reflection_instructions,
    answer_instructions,
)
from agent.utils import get_research_topic, parse_scientific_papers
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send
from agent.state import AgentState 
from agent.database import get_db_connection, Document

load_dotenv()

# Configuration
MAX_RESEARCH_LOOPS = 3
GEMINI_EMBEDDING_MODEL = "models/embedding-001"

# Initialize tools and services
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
embeddings = None # Lazy initialization to avoid event loop issues on startup

# Nodes
from agent.configuration import Configuration

# ... existing imports ...

def generate_initial_queries(state: AgentState, config: RunnableConfig) -> AgentState:
    """Generates the initial set of search queries based on the research topic."""
    print("---NODE: generate_initial_queries---")
    cfg = Configuration.from_runnable_config(config)
    research_topic = get_research_topic(state["messages"])
    prompt = query_writer_instructions.format(
        current_date=get_current_date(),
        research_topic=research_topic,
        number_queries=cfg.number_of_initial_queries,
    )
    response = completion(
        model=cfg.query_generator_model,
        messages=[{"content": prompt, "role": "user"}],
        response_format={"type": "json_object", "schema": SearchQueryList.model_json_schema()},
        api_key=GEMINI_API_KEY,
        num_retries=3
    )
    search_queries = SearchQueryList.model_validate_json(response.choices[0].message.content).query
    print(f"Generated initial queries: {search_queries}")
    return {"search_queries": search_queries, "research_topic": research_topic}


def continue_to_web_research(state: AgentState):
    """Conditional edge to start parallel searches."""
    print("---EDGE: continue_to_web_research---")
    # This returns a list of Send objects. Each Send object specifies the node
    # to call and the data to pass to it. This is the correct way to fan-out.
    return [Send("execute_searches", {"search_queries": [q]}) for q in state["search_queries"]]


def execute_searches(state: AgentState, config: RunnableConfig) -> AgentState:
    """Executes parallel searches for the given queries and returns ONLY the new results."""
    print(f"---NODE: execute_searches (Loop {state.get('research_loop_count', 0) + 1})---")
    search_queries = state["search_queries"]
    # This node should be stateless regarding past results.
    # It finds new abstracts and returns only them. The graph state handles aggregation.
    new_abstracts = []
    for query in search_queries:
        try:
            print(f"---TOOL: Running search for query: '{query}'---")
            # Clean the query for Arxiv tool
            cleaned_query = re.sub(r'"|AND|OR|[()]', '', query)
            print(f"---TOOL: Cleaned query for Arxiv: '{cleaned_query}'---")
            arxiv_response = arxiv_tool.invoke(cleaned_query)
            # Parse the raw string response
            parsed_papers = parse_scientific_papers(arxiv_response)
            new_abstracts.extend(parsed_papers)
        except Exception as e:
            print(f"---TOOL: Error during search for query: '{query}'. Error: {e}---")
            continue
    return {"literature_abstracts": new_abstracts}


def run_single_search(state: AgentState, config: RunnableConfig):
    """Runs a single academic search and returns the results."""
    query = state["query"]
    print(f"---TOOL: Running search for query: '{query}'---")
    arxiv_results = arxiv_tool.invoke(query)
    # Parse the raw string response and return the full dictionary
    parsed_papers = parse_scientific_papers(arxiv_results)
    return {"literature_abstracts": parsed_papers}


def reflection_and_refinement(state: AgentState, config: RunnableConfig) -> AgentState:
    """Reflects on the gathered abstracts and decides if more research is needed."""
    print("---NODE: reflection_and_refinement---")
    cfg = Configuration.from_runnable_config(config)
    # Extract summaries from the paper dictionaries for reflection
    summaries = [paper.get('summary', '') for paper in state["literature_abstracts"]]
    all_abstracts = "\n---\n".join(summaries)
    prompt = reflection_instructions.format(
        current_date=get_current_date(),
        research_topic=get_research_topic(state["messages"]),
        summaries=all_abstracts,
    )
    response = completion(
        model=cfg.reflection_model,
        messages=[{"content": prompt, "role": "user"}],
        response_format={"type": "json_object", "schema": Reflection.model_json_schema()},
        api_key=GEMINI_API_KEY,
        num_retries=3
    )
    reflection_result = Reflection.model_validate_json(response.choices[0].message.content)
    print(f"Reflection: Sufficient? {reflection_result.is_sufficient}. Gap: {reflection_result.knowledge_gap}")
    
    # Clear search queries if sufficient, otherwise use follow-up queries
    search_queries_to_return = []
    if not reflection_result.is_sufficient:
        search_queries_to_return = reflection_result.follow_up_queries or []

    return {
        "is_sufficient": reflection_result.is_sufficient,
        "knowledge_gap": reflection_result.knowledge_gap,
        "search_queries": search_queries_to_return,
        "research_loop_count": state.get("research_loop_count", 0) + 1,
    }

def should_continue_searching(state: AgentState):
    """Conditional edge to decide whether to continue the research loop."""
    print("---EDGE: should_continue_searching---")
    if state.get("is_sufficient") or state.get("research_loop_count", 0) >= MAX_RESEARCH_LOOPS:
        print("Conclusion: Research is sufficient or max loops reached.")
        return "automated_resource_management"
    else:
        print("Conclusion: Research is insufficient. Looping back for more searches.")
        return [Send("execute_searches", {"search_queries": [q]}) for q in state["search_queries"] if q]

def get_doi_from_title(title: str) -> str | None:
    """Queries the Crossref API to find a DOI for a given paper title."""
    print(f"---HELPER: Searching Crossref for title: '{title}'---")
    url = "https://api.crossref.org/works"
    params = {"query.title": title, "rows": 1, "select": "DOI"}
    headers = {"User-Agent": "RAGAcademicAgent/1.0 (mailto:your-email@example.com)"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        if data['message']['items']:
            doi = data['message']['items'][0].get('DOI')
            if doi:
                print(f"---HELPER: Found DOI: {doi}---")
                return doi
    except requests.exceptions.RequestException as e:
        print(f"---HELPER: Error querying Crossref API: {e}")
    except (KeyError, IndexError) as e:
        print(f"---HELPER: Could not parse DOI from Crossref response: {e}")
    
    print(f"---HELPER: No DOI found for title on Crossref.")
    return None

def automated_resource_management(state: AgentState, config: RunnableConfig) -> AgentState:
    """Stage 2: Fetches full-text resources and adds them to Zotero."""
    print("---NODE: automated_resource_management---")
    literature_full_text_urls = []
    for paper in state["literature_abstracts"]:
        paper_title = paper.get('title')
        if not paper_title:
            print("Skipping paper with no title.")
            continue

        doi = get_doi_from_title(paper_title)
        
        if doi:
            # Successfully found DOI, now proceed with Unpaywall and Zotero
            pdf_url_info = unpaywall_tool.invoke(doi)
            if "URL:" in pdf_url_info:
                pdf_url = pdf_url_info.split("URL: ")[1]
                literature_full_text_urls.append(pdf_url)
                print(f"Found PDF URL: {pdf_url}")

                paper_info = {"title": paper_title, "doi": doi}
                zotero_result = zotero_tool.invoke({"paper_info": paper_info})
                print(f"Zotero result: {zotero_result}")
            else:
                print(f"Unpaywall found no free PDF for DOI: {doi}")
        else:
            # Log and skip if no DOI was found
            print(f"No DOI found for title: '{paper_title}'. Skipping resource management for this paper.")

    return {"literature_full_text": literature_full_text_urls} # Pass URLs to next step


async def rag_based_knowledge_synthesis(state: AgentState, config: RunnableConfig) -> AgentState:
    """Stage 3: Chunks, embeds, and stores knowledge in a vector DB."""
    print("---NODE: rag_based_knowledge_synthesis---")
    global embeddings
    
    # Initialize embeddings within an async context if not already done
    if embeddings is None:
        print("Initializing embeddings service...")
        embeddings = GoogleGenerativeAIEmbeddings(model=GEMINI_EMBEDDING_MODEL, api_key=GEMINI_API_KEY)
    
    # Wrap synchronous DB and requests calls in asyncio.to_thread
    def process_pdfs_sync():
        db = get_db_connection()
        pdf_urls = state.get("literature_full_text", []) or []
        for i, url in enumerate(pdf_urls):
            try:
                print(f"Processing PDF: {url}")
                response = requests.get(url)
                response.raise_for_status() # Raises an HTTPError for bad responses
                # Open PDF from memory
                doc = fitz.open(stream=response.content, filetype="pdf")
                full_text = ""
                for page in doc:
                    full_text += page.get_text()
                doc.close()
                
                # 2. Chunk the text
                chunks = text_splitter.split_text(full_text)
                
                # 3. Generate embeddings
                chunk_embeddings = embeddings.embed_documents(chunks)
                
                # 4. Store in DB
                for chunk, embedding in zip(chunks, chunk_embeddings):
                    document = Document(content=chunk, embedding=embedding)
                    db.add(document)
                db.commit()
                print(f"Successfully processed and stored {len(chunks)} chunks for {url}")

            except Exception as e:
                print(f"Failed to process PDF at {url}. Error: {e}")
            finally:
                db.close()

            # Add a delay to avoid hitting API rate limits, but don't sleep after the last item
            if i < len(pdf_urls) - 1:
                print("Waiting for 20 seconds before processing the next PDF to respect API rate limits...")
                time.sleep(20)

    await asyncio.to_thread(process_pdfs_sync)
    return {}


def automated_report_generation(state: AgentState, config: RunnableConfig) -> AgentState:
    """Stage 4: Generates the final report based on the synthesized knowledge."""
    print("---NODE: automated_report_generation---")
    cfg = Configuration.from_runnable_config(config)

    # This is a simplified RAG retrieval. A real implementation would be more sophisticated.
    db = get_db_connection()
    try:
        # Use the session to query
        all_docs = db.query(Document).all()
        rag_context = "\n---\n".join([doc.content for doc in all_docs])
    finally:
        db.close()

    prompt = answer_instructions.format(
        current_date=get_current_date(),
        research_topic=get_research_topic(state["messages"]),
        summaries=rag_context, # Use the context from the DB
    )
    response = completion(
        model=cfg.answer_model,
        messages=[{"content": prompt, "role": "user"}],
        api_key=GEMINI_API_KEY,
        num_retries=3
    )
    report = response.choices[0].message.content
    return {"report": report, "messages": [AIMessage(content=report)]}


# Define the graph
builder = StateGraph(AgentState)

builder.add_node("generate_initial_queries", generate_initial_queries)
builder.add_node("execute_searches", execute_searches) # This will now be the parallel node
builder.add_node("reflection_and_refinement", reflection_and_refinement)
builder.add_node("automated_resource_management", automated_resource_management)
builder.add_node("rag_based_knowledge_synthesis", rag_based_knowledge_synthesis)
builder.add_node("automated_report_generation", automated_report_generation)

# Build the graph edges
builder.add_edge(START, "generate_initial_queries")

# This creates the parallel branching.
builder.add_conditional_edges(
    "generate_initial_queries",
    continue_to_web_research
)
builder.add_edge("execute_searches", "reflection_and_refinement")

builder.add_conditional_edges(
    "reflection_and_refinement",
    should_continue_searching,
)

builder.add_edge("automated_resource_management", "rag_based_knowledge_synthesis")
builder.add_edge("rag_based_knowledge_synthesis", "automated_report_generation")
builder.add_edge("automated_report_generation", END)

graph = builder.compile()
