import pytest
from unittest.mock import patch, MagicMock
from agent.tools_and_schemas import arxiv_tool, unpaywall_tool, zotero_tool

def test_arxiv_search_success():
    """
    Tests the arxiv_search tool for a successful API call.
    """
    # Mock the input query
    query = "test query"

    # Mock the expected response from the arxiv API
    mock_arxiv_response = [
        {"title": "Test Paper 1", "summary": "Summary of test paper 1."},
        {"title": "Test Paper 2", "summary": "Summary of test paper 2."},
    ]

    # Patch the arxiv.run method
    with patch("agent.tools_and_schemas.ArxivQueryRun") as MockArxivQueryRun:
        # Call the function to be tested
        result = arxiv_tool.invoke(query)

        # Assert that the arxiv.run method was called with the correct query
        MockArxivQueryRun.return_value.invoke.assert_called_once_with(query)

        # Assert that the result is in the expected format
        assert "documents" in result
        assert len(result["documents"]) == 2
        assert result["documents"][0].page_content == "Summary of test paper 1."
        assert result["documents"][0].metadata["title"] == "Test Paper 1"

def test_arxiv_search_no_results():
    """
    Tests the arxiv_search tool when the API returns no results.
    """
    query = "a query with no results"
    
    with patch("agent.tools_and_schemas.ArxivQueryRun") as MockArxivQueryRun:
        MockArxivQueryRun.return_value.invoke.return_value = []
        result = arxiv_tool.invoke(query)
        MockArxivQueryRun.return_value.invoke.assert_called_once_with(query)
        assert "documents" in result
        assert len(result["documents"]) == 0

def test_arxiv_search_api_error():
    """
    Tests the arxiv_search tool when the API raises an exception.
    """
    query = "a query that causes an error"

    with patch("agent.tools_and_schemas.arxiv_tool.invoke", side_effect=Exception("API Error")) as mock_arxiv_invoke:
        with pytest.raises(Exception, match="API Error"):
            arxiv_tool.invoke(query)
        MockArxivQueryRun.return_value.invoke.assert_called_once_with(query)


@patch('agent.tools_and_schemas.Unpywall.doi')
def test_unpaywall_tool_oa_found(mock_unpywall_doi):
    """Tests the unpaywall_tool when an open-access version is found."""
    doi = "10.1234/test.doi"
    # Create a mock DataFrame
    mock_df = MagicMock()
    mock_df.__getitem__.side_effect = lambda key: {'is_oa': [True], 'oa_status': ['gold'], 'best_oa_location.url': ['http://example.com/oa.pdf']}[key]
    mock_df.iloc = [mock_df] # Make iloc iterable and return the mock df

    mock_unpywall_doi.return_value = mock_df

    result = unpaywall_tool.invoke(doi)

    mock_unpywall_doi.assert_called_once_with(dois=[doi])
    assert "Open access version found!" in result
    assert "Status: gold" in result
    assert "URL: http://example.com/oa.pdf" in result

@patch('agent.tools_and_schemas.Unpywall.doi')
def test_unpaywall_tool_not_found(mock_unpywall_doi):
    """Tests the unpaywall_tool when no open-access version is found."""
    doi = "10.1234/closed.access"
    # Create a mock DataFrame
    mock_df = MagicMock()
    mock_df.__getitem__.side_effect = lambda key: {'is_oa': [False]}[key]
    mock_df.iloc = [mock_df] # Make iloc iterable and return the mock df
    mock_unpywall_doi.return_value = mock_df

    result = unpaywall_tool.invoke(doi)

    mock_unpywall_doi.assert_called_once_with(dois=[doi])
    assert result == "No open access version found for this DOI."

@patch('agent.tools_and_schemas.Unpywall.doi', side_effect=Exception("API Error"))
def test_unpaywall_tool_api_error(mock_unpywall_doi):
    """Tests the unpaywall_tool when the API call fails."""
    doi = "10.1234/error.doi"

    result = unpaywall_tool.invoke(doi)

    mock_unpywall_doi.assert_called_once_with(dois=[doi])
    assert "An error occurred: API Error" in result

@patch('agent.tools_and_schemas.zotero.Zotero')
def test_zotero_tool_success(mock_zotero_class):
    """Tests the zotero_tool for a successful item creation."""
    # Mock the Zotero instance and its methods
    mock_zot_instance = MagicMock()
    mock_zotero_class.return_value = mock_zot_instance
    mock_zot_instance.item_template.return_value = {'title': 'Test Paper'}
    mock_zot_instance.create_items.return_value = {'success': {'0': 'item-key'}, 'failed': {}}

    paper_info = {
        "title": "Test Paper",
        "authors": [{"creatorType": "author", "firstName": "John", "lastName": "Doe"}],
        "doi": "10.1234/test.doi"
    }

    result = zotero_tool.invoke(paper_info)

    mock_zotero_class.assert_called_once()
    mock_zot_instance.item_template.assert_called_once_with('journalArticle')
    mock_zot_instance.create_items.assert_called_once()
    assert "Successfully added paper 'Test Paper' to Zotero." in result

@patch('agent.tools_and_schemas.zotero.Zotero')
def test_zotero_tool_failure(mock_zotero_class):
    """Tests the zotero_tool for a failed item creation."""
    mock_zot_instance = MagicMock()
    mock_zotero_class.return_value = mock_zot_instance
    mock_zot_instance.item_template.return_value = {'title': 'Failed Paper'}
    mock_zot_instance.create_items.return_value = {'success': {}, 'failed': {'0': {'code': 400, 'message': 'Invalid field'}}}

    paper_info = {"title": "Failed Paper"}

    result = zotero_tool.invoke(paper_info)

    assert "Failed to add paper to Zotero" in result

@patch('agent.tools_and_schemas.zotero.Zotero', side_effect=Exception("API Key Invalid"))
def test_zotero_tool_api_error(mock_zotero_class):
    """Tests the zotero_tool when the Zotero API call fails."""
    paper_info = {"title": "Error Paper"}

    result = zotero_tool.invoke(paper_info)

    assert "An error occurred: API Key Invalid" in result