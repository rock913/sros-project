import os
import re
import requests
import fitz  # PyMuPDF
from typing import List
from agent.tools_and_schemas import SearchQueryList, Reflection, arxiv_tool, unpaywall_tool, zotero_tool
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, END, START
from langchain_core.runnables import RunnableConfig
from litellm import completion
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings


from agent.prompts import (
    get_current_date,
    query_writer_instructions,
    reflection_instructions,
    answer_instructions,
)
from agent.state import AgentState
from agent.database import get_db_connection, Document

load_dotenv()

# Configuration
MAX_RESEARCH_LOOPS = 3
GEMINI_EMBEDDING_MODEL = "models/embedding-001"

# Initialize tools and services
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
embeddings = GoogleGenerativeAIEmbeddings(model=GEMINI_EMBEDDING_MODEL, api_key=GEMINI_API_KEY)

# Nodes
def generate_initial_queries(state: AgentState, config: RunnableConfig) -> AgentState:
    """Generates the initial set of search queries based on the research topic."""
    print("---NODE: generate_initial_queries---")
    research_topic = state['messages'][-1].content
    prompt = query_writer_instructions.format(
        current_date=get_current_date(),
        research_topic=research_topic,
        number_queries=3,
    )
    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{"content": prompt, "role": "user"}],
        response_format={"type": "json_object", "schema": SearchQueryList.model_json_schema()},
        api_key=GEMINI_API_KEY
    )
    search_queries = SearchQueryList.model_validate_json(response.choices[0].message.content).query
    print(f"Generated initial queries: {search_queries}")
    return {
        "research_topic": research_topic,
        "search_queries": search_queries,
        "research_loop_count": 0,
        "literature_abstracts": [],
    }

def execute_searches(state: AgentState, config: RunnableConfig) -> AgentState:
    """Executes parallel searches for the given queries and aggregates results."""
    print(f"---NODE: execute_searches (Loop {state.get('research_loop_count', 0) + 1})---")
    search_queries = state["search_queries"]
    all_abstract_contents = state.get("literature_abstracts", [])
    for query in search_queries:
        print(f"---TOOL: Running search for query: '{query}'---")
        # arxiv_tool.invoke returns a dictionary like {"documents": [doc1, doc2]}
        arxiv_response = arxiv_tool.invoke(query)
        # Ensure arxiv_response is a dictionary and has 'documents' key
        if isinstance(arxiv_response, dict) and "documents" in arxiv_response:
            for doc in arxiv_response["documents"]:
                all_abstract_contents.append(doc.page_content)
        else:
            all_abstract_contents.append(str(arxiv_response))

    return {"literature_abstracts": all_abstract_contents}

def run_single_search(state: AgentState, config: RunnableConfig):
    """Runs a single academic search and returns the results."""
    query = state["query"]
    print(f"---TOOL: Running search for query: '{query}'---")
    arxiv_results = arxiv_tool.invoke(query)
    return {"literature_abstracts": [arxiv_results]}

def reflection_and_refinement(state: AgentState, config: RunnableConfig) -> AgentState:
    """Reflects on the gathered abstracts and decides if more research is needed."""
    print("---NODE: reflection_and_refinement---")
    print(f"Type of state['literature_abstracts']: {type(state['literature_abstracts'])}")
    print(f"Content of state['literature_abstracts']: {state['literature_abstracts']}")

    all_abstracts = "\n---\n".join([str(a) for a in state["literature_abstracts"]])
    prompt = reflection_instructions.format(
        current_date=get_current_date(),
        research_topic=state["research_topic"],
        summaries=all_abstracts,
    )
    response = completion(
        model="gemini/gemini-1.5-pro",
        messages=[{"content": prompt, "role": "user"}],
        response_format={"type": "json_object", "schema": Reflection.model_json_schema()},
        api_key=GEMINI_API_KEY
    )
    reflection_result = Reflection.model_validate_json(response.choices[0].message.content)
    print(f"Reflection: Sufficient? {reflection_result.is_sufficient}. Gap: {reflection_result.knowledge_gap}")
    return {
        "is_sufficient": reflection_result.is_sufficient,
        "knowledge_gap": reflection_result.knowledge_gap,
        "search_queries": reflection_result.follow_up_queries or [],
        "research_loop_count": state.get("research_loop_count", 0) + 1,
    }

def should_continue_searching(state: AgentState) -> str:
    """Conditional edge to decide whether to continue the research loop."""
    print("---EDGE: should_continue_searching---")
    if state["is_sufficient"] or state.get("research_loop_count", 0) >= MAX_RESEARCH_LOOPS:
        print("Conclusion: Research is sufficient or max loops reached.")
        return "automated_resource_management"
    else:
        print("Conclusion: Research is insufficient. Looping back.")
        return "execute_searches"

def automated_resource_management(state: AgentState, config: RunnableConfig) -> AgentState:
    """Stage 2: Fetches full-text resources and adds them to Zotero."""
    print("---NODE: automated_resource_management---")
    literature_full_text_urls = []
    for abstract in state["literature_abstracts"]:
        doi_match = re.search(r'10.\d{4,9}/[-._;()/:A-Z0-9]+', abstract, re.IGNORECASE)
        if doi_match:
            doi = doi_match.group(0)
            print(f"Found DOI: {doi}")
            pdf_url_info = unpaywall_tool.invoke(doi)
            if "URL:" in pdf_url_info:
                pdf_url = pdf_url_info.split("URL: ")[1]
                literature_full_text_urls.append(pdf_url)
                print(f"Found PDF URL: {pdf_url}")
                # Simplified paper_info for Zotero
                paper_info = {"title": abstract.split('\n')[0], "doi": doi}
                zotero_result = zotero_tool.invoke(paper_info)
                print(f"Zotero result: {zotero_result}")
        else:
            print("No DOI found in abstract.")
    return {"literature_full_text": literature_full_text_urls} # Pass URLs to next step

def rag_based_knowledge_synthesis(state: AgentState, config: RunnableConfig) -> AgentState:
    """Stage 3: Chunks, embeds, and stores knowledge in a vector DB."""
    print("---NODE: rag_based_knowledge_synthesis---")
    db = get_db_connection()
    try:
        pdf_urls = state.get("literature_full_text", [])
        for url in pdf_urls:
            try:
                print(f"Processing PDF: {url}")
                response = requests.get(url)
                response.raise_for_status()
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
    return {}

def automated_report_generation(state: AgentState, config: RunnableConfig) -> AgentState:
    """Stage 4: Generates the final report based on the synthesized knowledge."""
    print("---NODE: automated_report_generation---")
    # This is a simplified RAG retrieval. A real implementation would be more sophisticated.
    db = get_db_connection()
    try:
        all_docs = db.query(Document).all()
        rag_context = "\n---\n".join([doc.content for doc in all_docs])
    finally:
        db.close()

    prompt = answer_instructions.format(
        current_date=get_current_date(),
        research_topic=state["research_topic"],
        summaries=rag_context, # Use the context from the DB
    )
    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{"content": prompt, "role": "user"}],
        api_key=GEMINI_API_KEY
    )
    report = response.choices[0].message.content
    return {"report": report, "messages": [AIMessage(content=report)]}

# Define the graph
builder = StateGraph(AgentState)

builder.add_node("generate_initial_queries", generate_initial_queries)
builder.add_node("execute_searches", execute_searches)
builder.add_node("reflection_and_refinement", reflection_and_refinement)
builder.add_node("automated_resource_management", automated_resource_management)
builder.add_node("rag_based_knowledge_synthesis", rag_based_knowledge_synthesis)
builder.add_node("automated_report_generation", automated_report_generation)

# Build the graph edges
builder.add_edge(START, "generate_initial_queries")
builder.add_edge("generate_initial_queries", "execute_searches")
builder.add_edge("execute_searches", "reflection_and_refinement")

builder.add_conditional_edges(
    "reflection_and_refinement",
    should_continue_searching,
    {
        "execute_searches": "execute_searches",
        "automated_resource_management": "automated_resource_management",
    },
)

builder.add_edge("automated_resource_management", "rag_based_knowledge_synthesis")
builder.add_edge("rag_based_knowledge_synthesis", "automated_report_generation")
builder.add_edge("automated_report_generation", END)

graph = builder.compile()
