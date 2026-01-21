import pytest
from unittest.mock import MagicMock, patch

# Updated Imports to reflect the Architecture Shift
# The legacy tools in tools_and_schemas.py now delegate to our new domain Adapters.
# Therefore, we must mock the ADAPTERS, not the 'langchain' or 'pyzotero' internals,
# because tools_and_schemas.py no longer imports those directly.

from agent.tools_and_schemas import arxiv_tool, unpaywall_tool, zotero_tool

# --- Arxiv Tool Tests ---

@patch('agent.infrastructure.tools.arxiv_adapter.ArxivAdapter.search')
def test_arxiv_search_success(mock_search):
    """
    Tests the legacy arxiv_tool via the new ArxivAdapter delegation.
    """
    query = "test query"
    
    # Mocking Domain Objects return from Adapter
    # We need to simulate what ArxivAdapter.search returns (List[Paper])
    mock_paper1 = MagicMock()
    mock_paper1.publication_date.isoformat.return_value = "2023-01-01"
    mock_paper1.title = "Test Paper 1"
    mock_paper1.authors = ["Author A"]
    mock_paper1.abstract = "Abstract 1"

    mock_paper2 = MagicMock()
    mock_paper2.publication_date.isoformat.return_value = "2023-02-01"
    mock_paper2.title = "Test Paper 2"
    mock_paper2.authors = ["Author B"]
    mock_paper2.abstract = "Abstract 2"

    mock_search.return_value = [mock_paper1, mock_paper2]

    # Invoke the tool (which calls Adapter -> formats string)
    result = arxiv_tool.invoke(query)

    mock_search.assert_called_once_with(query, max_results=3)
    
    # Verify strict string formatting expected by parse_scientific_papers
    assert "Title: Test Paper 1" in result
    assert "Title: Test Paper 2" in result


@patch('agent.infrastructure.tools.arxiv_adapter.ArxivAdapter.search')
def test_arxiv_search_no_results(mock_search):
    """
    Tests the arxiv_search tool when the Adapter returns empty list.
    """
    query = "a query with no results"
    mock_search.return_value = []

    result = arxiv_tool.invoke(query)

    mock_search.assert_called_once_with(query, max_results=3)
    assert result == ""


@patch("agent.infrastructure.tools.arxiv_adapter.ArxivAdapter.search", side_effect=Exception("API Error"))
def test_arxiv_search_api_error(mock_search):
    """
    Tests the arxiv_search tool when the Adapter raises an exception.
    """
    query = "error query"
    result = arxiv_tool.invoke(query) # now returns string on error
    assert "Error executing arxiv search: API Error" in result


# --- Unpaywall Tool Tests ---

@patch('agent.infrastructure.tools.unpaywall_adapter.UnpaywallAdapter.fetch_by_doi')
def test_unpaywall_tool_oa_found(mock_fetch):
    """Tests the legacy unpaywall_tool via UnpaywallAdapter."""
    doi = "10.1234/test.doi"
    
    # Mock Domain Paper Object
    mock_paper = MagicMock()
    mock_paper.oa_info.is_oa = True
    mock_paper.oa_info.oa_status = 'gold'
    mock_paper.oa_info.oa_url = 'http://example.com/oa.pdf'
    
    mock_fetch.return_value = mock_paper

    result = unpaywall_tool.invoke(doi)

    mock_fetch.assert_called_once_with(doi)
    assert "Open access version found!" in result
    assert "Status: gold" in result
    assert "URL: http://example.com/oa.pdf" in result


@patch('agent.infrastructure.tools.unpaywall_adapter.UnpaywallAdapter.fetch_by_doi')
def test_unpaywall_tool_not_found(mock_fetch):
    """Tests the unpaywall_tool when Adapter returns None or non-OA paper."""
    doi = "10.1234/closed.access"
    
    # Case 1: Paper found but not OA
    mock_paper = MagicMock()
    mock_paper.oa_info.is_oa = False
    mock_fetch.return_value = mock_paper

    result = unpaywall_tool.invoke(doi)
    assert result == "No open access version found for this DOI."
    
    # Case 2: Paper not found (None)
    mock_fetch.return_value = None
    result = unpaywall_tool.invoke(doi)
    assert result == "No open access version found for this DOI."


@patch('agent.infrastructure.tools.unpaywall_adapter.UnpaywallAdapter.fetch_by_doi', side_effect=Exception("API Error"))
def test_unpaywall_tool_api_error(mock_fetch):
    """Tests exception handling."""
    doi = "10.1234/error.doi"

    result = unpaywall_tool.invoke(doi)

    assert "An error occurred: API Error" in result

# --- Zotero Tool Tests ---

@patch('agent.infrastructure.tools.zotero_adapter.ZoteroAdapter.save_paper')
def test_zotero_tool_success(mock_save):
    """Tests the legacy zotero_tool via ZoteroAdapter."""
    mock_save.return_value = "ITEM_KEY_123"
    
    # Legacy tool accepts a dict
    paper_info = {
        "title": "Test Paper",
        "authors": ["Author One"],
        "abstract": "Abstract",
        "date": "2023-01-01",
        "doi": "10.1000/xyz",
        "publication": "Publisher"
    }
    
    result = zotero_tool.invoke({"paper_info": paper_info})

    # Verify correct string formatting
    assert "Successfully added paper 'Test Paper' to Zotero" in result
    assert "Item Key: ITEM_KEY_123" in result


@patch('agent.infrastructure.tools.zotero_adapter.ZoteroAdapter.save_paper', side_effect=RuntimeError("Zotero Error"))
def test_zotero_tool_failure(mock_save):
    """Tests failure case."""
    paper_info = {"title": "Fail Paper"}
    
    result = zotero_tool.invoke({"paper_info": paper_info})
    assert "Failed to add paper to Zotero: Zotero Error" in result
