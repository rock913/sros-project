import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from agent.tools_and_schemas import arxiv_tool, pubmed_tool, unpaywall_tool, zotero_tool

@patch('agent.tools_and_schemas.arxiv_tool._run')
def test_arxiv_search_success(mock_arxiv_run):
    """
    Tests the arxiv_search tool for a successful API call.
    """
    query = "test query"
    mock_arxiv_run.return_value = {
        "documents": [
            MagicMock(page_content="Summary of test paper 1.", metadata={"title": "Test Paper 1"}),
            MagicMock(page_content="Summary of test paper 2.", metadata={"title": "Test Paper 2"}),
        ]
    }

    result = arxiv_tool.invoke(query)

    mock_arxiv_run.assert_called_once_with(query)
    assert "documents" in result
    assert len(result["documents"]) == 2
    assert result["documents"][0].page_content == "Summary of test paper 1."
    assert result["documents"][0].metadata["title"] == "Test Paper 1"

@patch('agent.tools_and_schemas.arxiv_tool._run')
def test_arxiv_search_no_results(mock_arxiv_run):
    """
    Tests the arxiv_search tool when the API returns no results.
    """
    query = "a query with no results"
    mock_arxiv_run.return_value = {"documents": []}

    result = arxiv_tool.invoke(query)

    mock_arxiv_run.assert_called_once_with(query)
    assert "documents" in result
    assert len(result["documents"]) == 0

@patch("agent.tools_and_schemas.arxiv_tool._run", side_effect=Exception("API Error"))
def test_arxiv_search_api_error(mock_arxiv_run):
    """
    Tests the arxiv_search tool when the API raises an exception.
    """
    query = "a query that causes an error"
    with pytest.raises(Exception, match="API Error"):
        arxiv_tool.invoke(query)
    mock_arxiv_run.assert_called_once_with(query)


@patch('agent.tools_and_schemas.Unpywall.doi')
def test_unpaywall_tool_oa_found(mock_unpywall_doi):
    """Tests the unpaywall_tool when an open-access version is found."""
    doi = "10.1234/test.doi"
    mock_df = pd.DataFrame([{
        'is_oa': True,
        'oa_status': 'gold',
        'best_oa_location.url': 'http://example.com/oa.pdf'
    }])
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
    mock_df = pd.DataFrame([{'is_oa': False}])
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
    mock_zot_instance = MagicMock()
    mock_zotero_class.return_value = mock_zot_instance
    mock_zot_instance.item_template.return_value = {'title': 'Test Paper'}
    mock_zot_instance.create_items.return_value = {'success': {'0': 'item-key'}, 'failed': {}}

    paper_info = {
        "title": "Test Paper",
        "authors": [{"creatorType": "author", "firstName": "John", "lastName": "Doe"}],
        "doi": "10.1234/test.doi"
    }

    result = zotero_tool.invoke({"paper_info": paper_info})

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

    result = zotero_tool.invoke({"paper_info": paper_info})

    assert "Failed to add paper to Zotero" in result

@patch('agent.tools_and_schemas.zotero.Zotero')
def test_zotero_tool_full_info_success(mock_zotero_class):
    """Tests the zotero_tool with a more complete paper_info dictionary."""
    mock_zot_instance = MagicMock()
    mock_zotero_class.return_value = mock_zot_instance
    mock_zot_instance.item_template.return_value = {'title': 'Full Info Paper'}
    mock_zot_instance.create_items.return_value = {'success': {'0': 'item-key'}, 'failed': {}}

    paper_info = {
        "title": "Full Info Paper",
        "authors": [{"creatorType": "author", "firstName": "Jane", "lastName": "Doe"}],
        "abstract": "This is an abstract.",
        "publication": "Journal of Testing",
        "volume": "1",
        "issue": "2",
        "pages": "10-20",
        "date": "2023-01-01",
        "doi": "10.1234/full.info.doi"
    }

    result = zotero_tool.invoke({"paper_info": paper_info})

    mock_zotero_class.assert_called_once()
    mock_zot_instance.item_template.assert_called_once_with('journalArticle')
    mock_zot_instance.create_items.assert_called_once()
    # Verify that item_template was called with the correct data
    args, kwargs = mock_zot_instance.create_items.call_args
    created_item = args[0][0]
    assert created_item['title'] == "Full Info Paper"
    assert created_item['creators'][0]['lastName'] == "Doe"
    assert created_item['abstractNote'] == "This is an abstract."
    assert created_item['publicationTitle'] == "Journal of Testing"
    assert created_item['volume'] == "1"
    assert created_item['issue'] == "2"
    assert created_item['pages'] == "10-20"
    assert created_item['date'] == "2023-01-01"
    assert created_item['DOI'] == "10.1234/full.info.doi"
    assert "Successfully added paper 'Full Info Paper' to Zotero." in result

@patch('agent.tools_and_schemas.zotero.Zotero', side_effect=Exception("API Key Invalid"))
def test_zotero_tool_api_error(mock_zotero_class):
    """Tests the zotero_tool when the Zotero API call fails."""
    paper_info = {"title": "Error Paper"}

    result = zotero_tool.invoke({"paper_info": paper_info})

    assert "An error occurred: API Key Invalid" in result

@patch('agent.tools_and_schemas.Unpywall.doi')
def test_unpaywall_tool_empty_df(mock_unpywall_doi):
    """Tests the unpaywall_tool when the API returns an empty DataFrame."""
    doi = "10.1234/empty.df"
    mock_df = pd.DataFrame([])
    mock_unpywall_doi.return_value = mock_df

    result = unpaywall_tool.invoke(doi)

    mock_unpywall_doi.assert_called_once_with(dois=[doi])
    assert result == "No open access version found for this DOI."

from agent.tools_and_schemas import SearchQueryList, Reflection, ResearchResult

def test_search_query_list_model():
    """Tests the SearchQueryList Pydantic model."""
    data = {"query": ["query1", "query2"], "rationale": "test rationale"}
    model = SearchQueryList(**data)
    assert model.query == ["query1", "query2"]
    assert model.rationale == "test rationale"

def test_reflection_model():
    """Tests the Reflection Pydantic model."""
    data = {"is_sufficient": True, "knowledge_gap": "", "follow_up_queries": []}
    model = Reflection(**data)
    assert model.is_sufficient == True
    assert model.knowledge_gap == ""
    assert model.follow_up_queries == []

def test_research_result_model():
    """Tests the ResearchResult Pydantic model."""
    data = {"summary": "test summary", "sources": ["source1", "source2"]}
    model = ResearchResult(**data)
    assert model.summary == "test summary"
    assert model.sources == ["source1", "source2"]

@patch('agent.tools_and_schemas.pubmed_tool._run')
def test_pubmed_search_success(mock_pubmed_run):
    """
    Tests the pubmed_tool for a successful API call.
    """
    query = "test query"
    mock_pubmed_run.return_value = {
        "documents": [
            MagicMock(page_content="Summary of test paper 1.", metadata={"title": "Test Paper 1"}),
            MagicMock(page_content="Summary of test paper 2.", metadata={"title": "Test Paper 2"}),
        ]
    }

    result = pubmed_tool.invoke(query)

    mock_pubmed_run.assert_called_once_with(query)
    assert "documents" in result
    assert len(result["documents"]) == 2
    assert result["documents"][0].page_content == "Summary of test paper 1."
    assert result["documents"][0].metadata["title"] == "Test Paper 1"

@patch('agent.tools_and_schemas.pubmed_tool._run')
def test_pubmed_search_no_results(mock_pubmed_run):
    """
    Tests the pubmed_tool when the API returns no results.
    """
    query = "a query with no results"
    mock_pubmed_run.return_value = {"documents": []}

    result = pubmed_tool.invoke(query)

    mock_pubmed_run.assert_called_once_with(query)
    assert "documents" in result
    assert len(result["documents"]) == 0

@patch("agent.tools_and_schemas.pubmed_tool._run", side_effect=Exception("API Error"))
def test_pubmed_search_api_error(mock_pubmed_run):
    """
    Tests the pubmed_tool when the API raises an exception.
    """
    query = "a query that causes an error"
    with pytest.raises(Exception, match="API Error"):
        pubmed_tool.invoke(query)
    mock_pubmed_run.assert_called_once_with(query)
