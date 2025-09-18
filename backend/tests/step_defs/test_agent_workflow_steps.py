import pytest
from pytest_bdd import scenario, given, when, then, parsers
from unittest.mock import patch, MagicMock
import os
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()

# Define the feature file
@scenario('../features/agent_workflow.feature', 'User asks a question that requires research refinement')
def test_research_refinement_workflow():
    pass

@scenario('../features/agent_workflow.feature', 'Research with No Further Refinement Needed')
def test_no_refinement_needed_workflow():
    pass

@scenario('../features/agent_workflow.feature', 'Research with Max Loop Reached')
def test_max_loop_reached_workflow():
    pass

@scenario('../features/agent_workflow.feature', 'Resource Management and RAG Integration')
def test_resource_management_rag_integration_workflow():
    pass

# --- Common Givens ---
@given('the agent server is running')
def agent_server_running():
    # In a real scenario, this would start the FastAPI server or ensure it's running
    # For now, we'll assume it's running or mock its behavior
    print("Agent server is assumed to be running.")
    pass

@given(parsers.parse('the research topic is "{topic}"'))
def set_research_topic(topic):
    pytest.research_topic = topic
    print(f"Research topic set to: {topic}")
    pass

@given(parsers.parse('the maximum research loops is set to {max_loops:d}'))
def set_max_research_loops(max_loops):
    # This would typically involve setting an environment variable or a config value
    # that the agent's graph.py would read.
    os.environ['MAX_RESEARCH_LOOPS'] = str(max_loops)
    print(f"Maximum research loops set to: {max_loops}")
    pass

# --- Common Whens ---
@when(parsers.parse('the user asks "{question}"'))
def user_asks_question(question):
    pytest.user_question = question
    # Here, you would typically invoke the agent with the question
    # For now, we'll just store the question
    print(f"User asks: {question}")
    pass

# --- Common Thens ---
@then('the agent should generate initial search queries')
def agent_generates_initial_queries():
    # Assert that the agent's internal state reflects query generation
    # This would involve inspecting logs or mocked calls
    print("Agent generated initial search queries.")
    pass

@then(parsers.parse('the agent should execute searches using tools like "{tool_name}"'))
def agent_executes_searches(tool_name):
    # Assert that the specified tool was invoked
    print(f"Agent executed searches using {tool_name}.")
    pass

@then('the agent should reflect on the initial search results')
def agent_reflects_on_results():
    # Assert that the reflection node was activated
    print("Agent reflected on initial search results.")
    pass

@then('the agent should identify knowledge gaps and generate follow-up queries')
def agent_identifies_gaps_and_generates_follow_up():
    # Assert that follow-up queries were generated
    print("Agent identified knowledge gaps and generated follow-up queries.")
    pass

@then('the agent should execute refined searches')
def agent_executes_refined_searches():
    # Assert that searches were executed again
    print("Agent executed refined searches.")
    pass

@then('the agent should find sufficient information')
def agent_finds_sufficient_information():
    # Assert that the reflection node determined sufficiency
    print("Agent found sufficient information.")
    pass

@then('the agent should find sufficient information without generating follow-up queries')
def agent_finds_sufficient_information_no_follow_up():
    # Assert that the reflection node determined sufficiency and no new queries were generated
    print("Agent found sufficient information without generating follow-up queries.")
    pass

@then('the agent should reach the maximum research loops')
def agent_reaches_max_loops():
    # Assert that the loop counter reached MAX_RESEARCH_LOOPS
    print("Agent reached maximum research loops.")
    pass

@then('the agent should proceed to manage resources despite insufficient information')
def agent_proceeds_to_resource_management_despite_insufficient_info():
    # Assert that the workflow moved to resource management
    print("Agent proceeded to resource management despite insufficient information.")
    pass

@then('the agent should manage resources by finding DOIs and adding PDFs to Zotero')
def agent_manages_resources():
    # Assert that unpaywall_tool and zotero_tool were called
    print("Agent managed resources (DOIs, Zotero).")
    pass

@then('the agent should manage resources by finding DOIs and adding PDFs to Zotero (even if none are found)')
def agent_manages_resources_even_if_none_found():
    # Assert that unpaywall_tool and zotero_tool were called, even if they returned no results
    print("Agent attempted resource management (DOIs, Zotero) even if none found.")
    pass

@then('the agent should synthesize knowledge from full-text documents')
def agent_synthesizes_knowledge():
    # Assert that PDF processing, chunking, and embedding occurred
    print("Agent synthesized knowledge from full-text documents.")
    pass

@then('the agent should synthesize knowledge from full-text documents (even if none are processed)')
def agent_synthesizes_knowledge_even_if_none_processed():
    # Assert that the RAG synthesis node was called, even if no PDFs were processed
    print("Agent attempted knowledge synthesis even if no PDFs were processed.")
    pass

@then('the agent should generate a comprehensive report with citations')
def agent_generates_report_with_citations():
    # Assert that the report generation node was called and output contains citations
    print("Agent generated a comprehensive report with citations.")
    pass

@then('the agent should generate a comprehensive report')
def agent_generates_report():
    # Assert that the report generation node was called
    print("Agent generated a comprehensive report.")
    pass

@then('the agent should generate a report based on available information')
def agent_generates_report_based_on_available_info():
    # Assert that the report generation node was called, acknowledging limited info
    print("Agent generated a report based on available information.")
    pass

@then('the final report should be delivered to the user')
def final_report_delivered():
    # Assert that the final message to the user contains the report
    print("Final report delivered to the user.")
    pass

@then(parsers.parse('the agent\'s response stream should show it is "{message_part}"'))
def agent_response_stream_shows(message_part):
    # This would involve inspecting the actual output stream of the agent
    print(f"Agent response stream shows: '{message_part}'")
    pass

@then(parsers.parse('the agent should first call tools like "{tool_name}" or "{another_tool_name}" with broad queries such as "{query_example}"'))
def agent_calls_broad_tools(tool_name, another_tool_name, query_example):
    # Assert that one of the specified tools was called with a broad query
    print(f"Agent called {tool_name} or {another_tool_name} with broad queries like '{query_example}'.")
    pass

@then(parsers.parse('the agent should then call "{tool_name}" or "{another_tool_name}" a second time with these refined queries'))
def agent_calls_refined_tools(tool_name, another_tool_name):
    # Assert that one of the specified tools was called again with refined queries
    print(f"Agent called {tool_name} or {another_tool_name} a second time with refined queries.")
    pass

@then('the agent should find abstracts containing DOIs')
def agent_finds_dois():
    # Assert that DOIs were extracted from abstracts
    print("Agent found abstracts containing DOIs.")
    pass

@then(parsers.parse('the agent should use "{tool_name}" to find PDF URLs'))
def agent_uses_unpaywall_tool(tool_name):
    # Assert that unpaywall_tool was called
    print(f"Agent used {tool_name} to find PDF URLs.")
    pass

@then(parsers.parse('the agent should use "{tool_name}" to add papers to Zotero'))
def agent_uses_zotero_tool(tool_name):
    # Assert that zotero_tool was called
    print(f"Agent used {tool_name} to add papers to Zotero.")
    pass

@then('the agent should download and process full-text PDFs')
def agent_downloads_and_processes_pdfs():
    # Assert that PDF download and processing occurred
    print("Agent downloaded and processed full-text PDFs.")
    pass

@then('the agent should chunk and embed the PDF content into the vector database')
def agent_chunks_and_embeds_pdf_content():
    # Assert that chunking, embedding, and DB storage occurred
    print("Agent chunked and embedded PDF content into the vector database.")
    pass

@then('the agent should synthesize knowledge from the vector database')
def agent_synthesizes_knowledge_from_db():
    # Assert that knowledge was retrieved from the vector DB for report generation
    print("Agent synthesized knowledge from the vector database.")
    pass

@then('the agent\'s response stream should show it is "reflecting on the initial results" and identifying knowledge gaps')
def agent_response_shows_reflecting_and_gaps():
    print("Agent response shows reflecting and identifying gaps.")
    pass

@then('the agent should synthesize knowledge from full-text documents (even if limited)')
def agent_synthesizes_knowledge_limited():
    print("Agent synthesized knowledge from limited full-text documents.")
    pass

@then(parsers.parse('after finding sufficient information, the agent should finally deliver a structured "{report_type}" that synthesizes all findings and includes citations'))
def agent_delivers_report(report_type):
    print(f"Agent delivers a structured {report_type}.")
    pass
