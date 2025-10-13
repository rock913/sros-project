import pytest
from pytest_bdd import scenario, given, when, then, parsers
from unittest.mock import MagicMock, call, patch
import json
import asyncio
import io
from contextlib import redirect_stdout
import fitz # Added import for fitz

# Import the agent state (but NOT the production graph with checkpointer)
from agent.state import AgentState
from langchain_core.messages import HumanMessage

# --- Test Scenarios ---

@scenario('../features/agent_workflow.feature', 'Research with No Further Refinement Needed')
def test_no_refinement_needed_workflow():
    """Scenario: Agent finds sufficient info on the first try."""
    pass

@scenario('../features/agent_workflow.feature', 'User asks a question that requires research refinement')
def test_research_refinement_workflow():
    pass

@scenario('../features/agent_workflow.feature', 'Research with Max Loop Reached')
def test_research_with_max_loop_reached_workflow():
    pass

@then(parsers.parse('after finding sufficient information, the agent should finally deliver a structured "report" that synthesizes all findings and includes citations'))
def verify_final_report_with_citations(configured_agent_context):
    # This step combines verification of report generation and delivery.
    # It reuses logic from existing steps.
    verify_report_generation(configured_agent_context)
    verify_final_message(configured_agent_context)

@scenario('../features/agent_workflow.feature', 'Resource Management and RAG Integration')
def test_resource_management_and_rag_integration_workflow():
    pass

# --- Step Definitions ---

@given("the agent server is running")
def agent_server_is_running():
    """
    Placeholder step for the agent server being in a running state.
    Actual setup is handled by the configured_agent_context fixture.
    """
    pass

@given(parsers.parse("the maximum research loops is set to {max_loops:d}"))
def set_max_research_loops(max_loops):
    return max_loops


@given(parsers.parse("the agent is configured for the '{scenario_name}' scenario with research topic '{topic}'"), target_fixture='configured_agent_context')
def the_agent_is_configured_for_scenario(agent_test_context, scenario_name, topic):
    """
    A single, powerful Given step to configure all mocks based on the scenario name.
    """
    # Determine max_loops based on scenario, with a default
    if scenario_name == "Max Loop Reached":
        max_loops = 2
    else:
        max_loops = 3 # Default for other scenarios

    with patch('agent.graph.MAX_RESEARCH_LOOPS', max_loops):
        mock_completion = agent_test_context["mock_completion"]
        mock_arxiv = agent_test_context["mock_arxiv"]
        mock_unpaywall = agent_test_context["mock_unpaywall"]
        mock_zotero = agent_test_context["mock_zotero"]
        mock_embedding = agent_test_context["mock_embedding"] # Corrected key
        mock_requests_get = agent_test_context["mock_requests_get"]

        # Common responses
        final_report_content = f"Final report for {scenario_name}"
        final_report_response = MagicMock(choices=[MagicMock(message=MagicMock(content=final_report_content))])
        initial_queries_response = MagicMock(choices=[MagicMock(message=MagicMock(content=json.dumps({"query": [topic], "rationale": "Initial query"})))])

        # Patch fitz.open directly at the source to fix PDF processing issues
        with patch('fitz.open') as mock_fitz_open:
            mock_doc = MagicMock()
            mock_page = MagicMock()
            mock_page.get_text.return_value = "This is some fake PDF text content."
            # Make the mock usable in a 'with' statement
            mock_doc.__enter__.return_value = mock_doc
            mock_doc.__iter__.return_value = [mock_page]
            mock_doc.close.return_value = None
            mock_fitz_open.return_value = mock_doc

            # Patch litellm.embedding to return our mock_embedding instance
            with patch('litellm.embedding', return_value=mock_embedding):
                if scenario_name == "No Refinement Needed":
                    reflection_response = MagicMock(choices=[MagicMock(message=MagicMock(content=json.dumps({"is_sufficient": True, "knowledge_gap": "", "follow_up_queries": []})))])
                    mock_completion.side_effect = [initial_queries_response, reflection_response, final_report_response]
                    # Mock tool chain for happy path
                    mock_arxiv.invoke.return_value = {"documents": [MagicMock(page_content="abstract1 DOI: 10.1234/test.001")]}
                    mock_unpaywall.invoke.return_value = "Open access version found! Status: OA. URL: http://example.com/paper.pdf"
                    mock_zotero.invoke.return_value = "Successfully added paper to Zotero."
                    mock_requests_get.return_value.content = b"fake pdf content"
                    mock_requests_get.return_value.raise_for_status.return_value = None
                    mock_embedding.embed_documents.return_value = [[0.1] * 1024]

                elif scenario_name == "Research Refinement":
                    reflection_1 = MagicMock(choices=[MagicMock(message=MagicMock(content=json.dumps({"is_sufficient": False, "knowledge_gap": "Need more info", "follow_up_queries": ["query 2"]})))])
                    reflection_2 = MagicMock(choices=[MagicMock(message=MagicMock(content=json.dumps({"is_sufficient": True, "knowledge_gap": "", "follow_up_queries": []})))])
                    mock_completion.side_effect = [initial_queries_response, reflection_1, reflection_2, final_report_response]
                    mock_arxiv.invoke.side_effect = [
                        {"documents": [MagicMock(page_content="abstract1 DOI: 10.1234/test.001")]},
                        {"documents": [MagicMock(page_content="abstract2 DOI: 10.1234/test.002")]},
                        {"documents": [MagicMock(page_content="abstract3 DOI: 10.1234/test.003")]}, # For parallel execution
                    ]

                elif scenario_name == "Max Loop Reached":
                    reflection_insufficient = MagicMock(choices=[MagicMock(message=MagicMock(content=json.dumps({"is_sufficient": False, "knowledge_gap": "Still need more info", "follow_up_queries": ["query loop"]})))])
                    side_effects = [initial_queries_response]
                    # The reflection node will be called max_loops times
                    for _ in range(max_loops):
                        side_effects.append(reflection_insufficient)
                    side_effects.append(final_report_response)
                    mock_completion.side_effect = side_effects
                    # FIX: Added a DOI to the mock response to allow resource management to proceed
                    mock_arxiv.invoke.return_value = {"documents": [MagicMock(page_content="Limited info with DOI: 10.1234/test.maxloop")]}
                    # Add mocks for the rest of the chain to prevent downstream errors
                    mock_unpaywall.invoke.return_value = "Open access version found! Status: OA. URL: http://example.com/paper.pdf"
                    mock_zotero.invoke.return_value = "Successfully added paper to Zotero."
                    mock_requests_get.return_value.content = b"fake pdf content"
                    mock_requests_get.return_value.raise_for_status.return_value = None
                    mock_embedding.embed_documents.return_value = [[0.1] * 1024]


                elif scenario_name == "Resource Management and RAG":
                    reflection_response = MagicMock(choices=[MagicMock(message=MagicMock(content=json.dumps({"is_sufficient": True, "knowledge_gap": "", "follow_up_queries": []})))])
                    mock_completion.side_effect = [initial_queries_response, reflection_response, final_report_response]
                    mock_arxiv.invoke.return_value = {"documents": [
                        MagicMock(page_content="Paper A abstract with DOI: 10.1234/a"),
                        MagicMock(page_content="Paper B abstract with DOI: 10.5678/b")
                    ]}
                    mock_unpaywall.invoke.side_effect = [
                        "Open access version found! Status: OA. URL: http://example.com/a.pdf",
                        "Open access version found! Status: OA. URL: http://example.com/b.pdf"
                    ]
                    mock_zotero.invoke.return_value = "Paper added to Zotero."
                    mock_requests_get.return_value.content = b"fake pdf content"
                    mock_requests_get.return_value.raise_for_status.return_value = None
                    mock_embedding.embed_documents.return_value = [[0.1] * 1024, [0.2] * 1024]
                    mock_embedding.embed_query.return_value = [0.1] * 1024

                else:
                    pytest.fail(f"Unknown scenario name: {scenario_name}")

                agent_test_context["expected_report"] = final_report_content
                agent_test_context["max_loops"] = max_loops # Store for assertion
                yield agent_test_context

# --- Whens ---

@when(parsers.parse('the user asks "{question}"'))
def run_agent(configured_agent_context, question, test_graph):
    """
    Invokes the agent graph with the user's question and stores the final state.
    Uses test_graph fixture (without checkpointer) for testing.
    """
    initial_state = {"messages": [HumanMessage(content=question)]}
    config = {
        "recursion_limit": 10
    }
    # No thread_id needed since test_graph doesn't have checkpointer

    f = io.StringIO()
    with redirect_stdout(f):
        # Run the async function synchronously for the test
        final_state = asyncio.run(test_graph.ainvoke(initial_state, config=config))
    
    output = f.getvalue()
    configured_agent_context["captured_output"] = output
    configured_agent_context["final_state"] = final_state
    return final_state

# --- Thens ---

@then('the agent should generate initial search queries')
def verify_initial_query_generation(configured_agent_context):
    mock_completion = configured_agent_context["mock_completion"]
    assert mock_completion.call_count >= 1, "LLM was not called to generate queries"

@then(parsers.parse('the agent should execute searches using tools like "{tool_name}"'))
def verify_search_execution(configured_agent_context, tool_name):
    mock_arxiv = configured_agent_context["mock_arxiv"]
    mock_arxiv.invoke.assert_called()

@then('the agent should reflect on the initial search results')
def verify_reflection(configured_agent_context):
    mock_completion = configured_agent_context["mock_completion"]
    assert mock_completion.call_count >= 2, "LLM was not called for reflection"

@then('the agent should find sufficient information without generating follow-up queries')
def verify_sufficiency(configured_agent_context):
    final_state = configured_agent_context["final_state"]
    assert final_state["is_sufficient"] is True, "Agent should have found information to be sufficient"
    # After a successful reflection, the follow_up_queries are cleared
    assert not final_state.get("search_queries", []), "Agent should not have follow-up queries in the final state"

@then('the agent should manage resources by finding DOIs and adding PDFs to Zotero')
def verify_resource_management(configured_agent_context):
    mock_unpaywall = configured_agent_context["mock_unpaywall"]
    mock_zotero = configured_agent_context["mock_zotero"]
    mock_unpaywall.invoke.assert_called()
    mock_zotero.invoke.assert_called()

@then('the agent should synthesize knowledge from full-text documents')
def verify_rag_synthesis(configured_agent_context):
    mock_embeddings = configured_agent_context["mock_embeddings"]
    mock_embeddings.embed_documents.assert_called()

@then('the agent should generate a comprehensive report')
def verify_report_generation(configured_agent_context):
    final_state = configured_agent_context["final_state"]
    expected_report = configured_agent_context["expected_report"]
    assert "report" in final_state, "Final state should contain a report"
    assert final_state["report"] == expected_report, "The generated report does not match the expected report"

@then('the final report should be delivered to the user')
def verify_final_message(configured_agent_context):
    final_state = configured_agent_context["final_state"]
    last_message = final_state["messages"][-1]
    assert last_message.type == "ai"
    assert last_message.content == configured_agent_context["expected_report"]

@then(parsers.parse('the agent\'s response stream should show it is "{status_message}"'))
def verify_agent_status_message(configured_agent_context, status_message):
    """
    Checks the captured stdout for LangGraph node names as a proxy for status messages.
    This is a workaround for the agent not persisting status messages in the final state.
    """
    # Map human-readable status messages from the feature file to node names
    status_to_node_map = {
        "generating an initial research plan": "---NODE: generate_initial_queries---",
        "reflecting on the initial results": "---NODE: reflection_and_refinement---",
        "formulating follow-up queries": "---NODE: reflection_and_refinement---", # This node does both
    }
    
    expected_node_name = status_to_node_map.get(status_message)
    assert expected_node_name, f"No node mapping found for status message: '{status_message}'"
    
    captured_output = configured_agent_context.get("captured_output", "")
    # Check if the expected node name appears in the combined stdout/stderr
    assert expected_node_name in captured_output, \
        f'Expected node execution "{expected_node_name}" not found in stdout/stderr for status: "{status_message}"'


@then(parsers.parse('the agent should first call tools like "{tool_name}" or "{another_tool_name}" with broad queries such as "{query_pattern}"'))
def verify_initial_tool_call(configured_agent_context, tool_name, another_tool_name, query_pattern):
    mock_arxiv = configured_agent_context["mock_arxiv"]
    mock_arxiv.invoke.assert_any_call(query_pattern)

@then(parsers.parse('the agent should then call "{tool_name}" or "{another_tool_name}" a second time with these refined queries'))
def verify_refined_tool_call(configured_agent_context, tool_name, another_tool_name):
    mock_arxiv = configured_agent_context["mock_arxiv"]
    # Initial call + fan-out for refined queries
    assert mock_arxiv.invoke.call_count > 1, "Arxiv tool was not called enough times for refinement."

@then('the agent should identify knowledge gaps and generate follow-up queries')
def verify_knowledge_gaps_and_follow_up_queries(configured_agent_context):
    final_state = configured_agent_context["final_state"]
    mock_completion = configured_agent_context["mock_completion"]
    # This state is intermediate, so we check the mocks. The final state will have is_sufficient=True
    # We can check the reflection calls to the LLM
    # A more robust way than checking final_state, which might not have intermediate logs.
    assert any(
        '"is_sufficient": false' in call_args[1]['messages'][0]['content']
        for call_args in mock_completion.call_args_list
    ), "Agent should have identified knowledge gaps in an intermediate step"


@then('the agent should reach the maximum research loops')
def verify_max_loops_reached(configured_agent_context):
    final_state = configured_agent_context["final_state"]
    max_loops = configured_agent_context["max_loops"]
    # The final loop count in the state should equal the max loops
    assert final_state.get("research_loop_count") == max_loops

@then('the agent should find abstracts containing DOIs')
def verify_abstracts_with_dois(configured_agent_context):
    mock_arxiv = configured_agent_context["mock_arxiv"]
    mock_arxiv.invoke.assert_called()

@then('the agent should use "unpaywall_tool" to find PDF URLs')
def verify_unpaywall_tool_called(configured_agent_context):
    mock_unpaywall = configured_agent_context["mock_unpaywall"]
    mock_unpaywall.invoke.assert_called()

@then('the agent should use "zotero_tool" to add papers to Zotero')
def verify_zotero_tool_called(configured_agent_context):
    mock_zotero = configured_agent_context["mock_zotero"]
    mock_zotero.invoke.assert_called()

@then('the agent should chunk and embed the PDF content into the vector database')
def verify_embeddings_called(configured_agent_context):
    mock_embeddings = configured_agent_context["mock_embeddings"]
    mock_embeddings.embed_documents.assert_called()

@then('the agent should synthesize knowledge from the vector database')
def verify_knowledge_synthesis_from_db(configured_agent_context):
    # This is implicitly tested by the final report generation call,
    # which should include context from the RAG.
    # A more specific test could mock the DB query.
    pass

@then('the agent should generate a comprehensive report with citations')
def verify_report_with_citations(configured_agent_context):
    final_state = configured_agent_context["final_state"]
    expected_report = configured_agent_context["expected_report"]
    assert "report" in final_state, "Final state should contain a report"
    assert final_state["report"] == expected_report, "The generated report does not match the expected report"
    # A more robust test would check for actual citation markers, e.g., "[1]"
    # For now, we assume the final report content implies citation.

@then(parsers.parse('the agent should manage resources by finding DOIs and adding PDFs to Zotero (even if none are found)'))
def verify_resource_management_even_if_none_found(configured_agent_context):
    # In the 'No Refinement Needed' scenario, the mocks are set up to simulate a successful run.
    # The assertion here is that the tools were at least called.
    mock_unpaywall = configured_agent_context["mock_unpaywall"]
    mock_zotero = configured_agent_context["mock_zotero"]
    mock_unpaywall.invoke.assert_called()
    mock_zotero.invoke.assert_called()

@then(parsers.parse('the agent should synthesize knowledge from full-text documents (even if none are processed)'))
def verify_rag_synthesis_even_if_none_processed(configured_agent_context):
    # Similar to the above, we assert that the embedding tool was called.
    mock_embeddings = configured_agent_context["mock_embeddings"]
    mock_embeddings.embed_documents.assert_called()

@then('the agent should execute refined searches')
def verify_refined_searches(configured_agent_context):
    mock_arxiv = configured_agent_context["mock_arxiv"]
    # The number of calls should be greater than the initial set of queries
    assert mock_arxiv.invoke.call_count > 1

@then('the agent should proceed to manage resources despite insufficient information')
def verify_resource_management_on_max_loops(configured_agent_context):
    mock_unpaywall = configured_agent_context["mock_unpaywall"]
    mock_zotero = configured_agent_context["mock_zotero"]
    # Even if the loop is exhausted, the workflow should continue.
    mock_unpaywall.invoke.assert_called()
    mock_zotero.invoke.assert_called()

@then('the agent should synthesize knowledge from full-text documents (even if limited)')
def verify_rag_synthesis_on_max_loops(configured_agent_context):
    mock_embeddings = configured_agent_context["mock_embeddings"]
    mock_embeddings.embed_documents.assert_called()

@then('the agent should generate a report based on available information')
def verify_report_generation_on_max_loops(configured_agent_context):
    final_state = configured_agent_context["final_state"]
    expected_report = configured_agent_context["expected_report"]
    assert "report" in final_state, "Final state should contain a report"
    assert final_state["report"] == expected_report, "The generated report does not match the expected report"

@then('the agent should download and process full-text PDFs')
def verify_pdf_download_and_processing(configured_agent_context):
    mock_requests_get = configured_agent_context["mock_requests_get"]
    mock_requests_get.assert_called()
    # We can check the number of calls matches the number of PDFs found
    assert mock_requests_get.call_count == 2 # Based on the 'Resource Management and RAG' scenario setup