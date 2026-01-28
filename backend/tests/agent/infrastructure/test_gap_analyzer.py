import pytest
from unittest.mock import AsyncMock, Mock, patch
from agent.domain.schemas.draft import DraftContext, EvidenceGap
from agent.domain.ports.gap_analyzer import IGapAnalyzer
from agent.infrastructure.nodes.gap_analyzer import GapAnalyzerAdapter  # Import when created


@pytest.fixture
def mock_llm_adapter():
    """Mock LLM adapter for isolated testing."""
    mock = AsyncMock()
    mock.completion.return_value = Mock(content="""
    [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "context_snippet": "Transformer models are very fast.",
            "missing_information": "Empirical data supporting speed claims",
            "search_queries": ["transformer inference speed benchmarks"],
            "confidence": 0.8
        }
    ]
    """)
    return mock


@pytest.fixture
def gap_analyzer(mock_llm_adapter) -> IGapAnalyzer:
    """Factory for GapAnalyzerAdapter with mocked dependencies."""
    return GapAnalyzerAdapter(llm_adapter=mock_llm_adapter)


class TestGapAnalyzerContract:
    """Test IGapAnalyzer contract adherence via GapAnalyzerAdapter implementation."""

    @pytest.mark.asyncio
    async def test_empty_draft_returns_empty_gaps(self, gap_analyzer: IGapAnalyzer, mock_llm_adapter):
        """Test Scenario 1: Empty draft returns empty gap list."""
        context = DraftContext(content="")
        mock_llm_adapter.generate.return_value = Mock(content="[]")

        result = await gap_analyzer.analyze(context)

        assert result == []
        mock_llm_adapter.generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_claim_without_evidence_creates_gap(self, gap_analyzer: IGapAnalyzer, mock_llm_adapter):
        """Test Scenario 2: Claim without evidence creates gap."""
        context = DraftContext(content="Transformer models are very fast.")
        mock_llm_adapter.generate.return_value = Mock(content="""
        [
            {
                "context_snippet": "Transformer models are very fast.",
                "missing_information": "Empirical data supporting speed claims compared to RNNs",
                "search_queries": ["transformer vs rnn inference speed comparison", "transformer model benchmarks"],
                "confidence": 0.85
            }
        ]
        """)

        result = await gap_analyzer.analyze(context)

        assert len(result) == 1
        gap = result[0]
        assert isinstance(gap, EvidenceGap)
        assert "speed" in gap.missing_information.lower()
        assert len(gap.search_queries) > 0
        assert 0.0 <= gap.confidence <= 1.0

    @pytest.mark.asyncio
    async def test_well_cited_content_returns_no_gaps(self, gap_analyzer: IGapAnalyzer, mock_llm_adapter):
        """Test Scenario 3: Well-cited content returns no gaps."""
        context = DraftContext(content="Transformer speed is proven [@Vaswani2017, @Brown2020]")
        mock_llm_adapter.generate.return_value = Mock(content="[]")

        result = await gap_analyzer.analyze(context)

        assert result == []

    @pytest.mark.asyncio
    async def test_multiple_gaps_identified(self, gap_analyzer: IGapAnalyzer, mock_llm_adapter):
        """Test Scenario 4: Multiple gaps identified."""
        context = DraftContext(content="""
        Transformer models are very fast. They use attention mechanisms.
        RNN models are slower but more interpretable. Large language models excel at generation.
        """)
        mock_llm_adapter.generate.return_value = Mock(content="""
        [
            {
                "context_snippet": "Transformer models are very fast.",
                "missing_information": "Benchmark data comparing transformer inference speed",
                "search_queries": ["transformer inference speed benchmarks"],
                "confidence": 0.8
            },
            {
                "context_snippet": "RNN models are slower but more interpretable.",
                "missing_information": "Evidence for RNN interpretability advantages",
                "search_queries": ["rnn interpretability studies"],
                "confidence": 0.7
            },
            {
                "context_snippet": "Large language models excel at generation.",
                "missing_information": "Generation quality metrics or examples",
                "search_queries": ["large language model generation evaluation"],
                "confidence": 0.6
            }
        ]
        """)

        result = await gap_analyzer.analyze(context)

        assert len(result) == 3
        for gap in result:
            assert isinstance(gap, EvidenceGap)
            assert gap.search_queries
            assert 0.0 <= gap.confidence <= 1.0

    @pytest.mark.asyncio
    async def test_focus_cursor_analysis(self, gap_analyzer: IGapAnalyzer, mock_llm_adapter):
        """Test Scenario 5: Focus cursor analysis."""
        content = "Line 1: Transformers are fast.\nLine 2: RNNs are accurate.\nLine 3: LLMs can reason."
        context = DraftContext(content=content, cursor_position=(1, 10))  # Cursor on line 1
        mock_llm_adapter.generate.return_value = Mock(content="""
        [
            {
                "context_snippet": "Line 1: Transformers are fast.",
                "missing_information": "Speed metric data",
                "search_queries": ["transformer speed metrics"],
                "confidence": 0.9
            }
        ]
        """)

        # The LLM should receive cursor context to prioritize analysis
        result = await gap_analyzer.analyze(context)

        assert len(result) == 1
        # In implementation, we'd verify cursor info was passed to LLM prompt

    @pytest.mark.asyncio
    async def test_evidence_gap_validation(self, gap_analyzer: IGapAnalyzer, mock_llm_adapter):
        """Test EvidenceGap validation and properties."""
        context = DraftContext(content="Transformers are efficient.")
        mock_llm_adapter.generate.return_value = Mock(content="""
        [
            {
                "context_snippet": "Transformers are efficient.",
                "missing_information": "Efficiency metrics",
                "search_queries": ["transformer efficiency benchmarks"],
                "confidence": 0.8
            }
        ]
        """)

        result = await gap_analyzer.analyze(context)

        gap = result[0]
        assert gap.is_high_confidence  # confidence >= 0.7
        assert len(gap.context_snippet) <= 500  # Max length constraint
        assert len(gap.search_queries) > 0


class TestGapAnalyzerEnvironmentIsolation:
    """Test environment isolation - no external API calls."""

    def test_no_http_calls_in_constructor(self):
        """Adapter construction should not make external calls."""
        mock_llm = Mock()
        adapter = GapAnalyzerAdapter(llm_adapter=mock_llm)

        # No external calls should be made during construction
        assert not mock_llm.called
        assert adapter.llm_adapter == mock_llm

    @patch.dict('os.environ', {}, clear=True)
    def test_no_environment_dependencies(self):
        """Adapter should work without env vars (fully mocked)."""
        # This would fail if adapter tried to access env vars
        mock_llm = Mock()
        adapter = GapAnalyzerAdapter(llm_adapter=mock_llm)

        assert adapter is not None


class TestGapAnalyzerPromptEngineering:
    """Test LLM prompt structure and academic reviewer role."""

    @pytest.mark.asyncio
    async def test_academic_reviewer_prompt(self, gap_analyzer: IGapAnalyzer, mock_llm_adapter):
        """Verify LLM receives academic reviewer prompt."""
        context = DraftContext(content="Transformers enable parallel processing.")
        mock_llm_adapter.generate.return_value = Mock(content="[]")

        await gap_analyzer.analyze(context)

        call_args = mock_llm_adapter.generate.call_args
        prompt = call_args[1]['messages'][0]['content']

        assert "Academic Reviewer" in prompt
        assert "identify evidence gaps" in prompt.lower()
        assert "research draft" in prompt.lower()
        assert "critically examine" in prompt.lower()

    @pytest.mark.asyncio
    async def test_json_structured_output(self, gap_analyzer: IGapAnalyzer, mock_llm_adapter):
        """Verify LLM is instructed to return structured JSON."""
        context = DraftContext(content="Test content")
        mock_llm_adapter.generate.return_value = Mock(content="""
        [
            {
                "context_snippet": "Test content",
                "missing_information": "Test gap",
                "search_queries": ["test query"],
                "confidence": 0.5
            }
        ]
        """)

        result = await gap_analyzer.analyze(context)

        assert len(result) == 1
        assert result[0].missing_information == "Test gap"

        # Verify call requested JSON structure
        call_args = mock_llm_adapter.generate.call_args
        prompt = call_args[1]['messages'][0]['content']
        assert "JSON array" in prompt or "json" in prompt.lower()
