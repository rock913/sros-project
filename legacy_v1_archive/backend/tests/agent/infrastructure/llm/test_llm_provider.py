"""
Tests for LLM Provider Infrastructure

This module tests the LitellmProvider implementation using strict isolation principles.
All external dependencies (APIs, file I/O, environment variables) are mocked using unittest.mock.

@Infrastructure Testing Principles:
- Unit tests must be environment-agnostic (no API keys, no network calls)
- Mock ALL external I/O: litellm.completion, os.getenv, file operations
- Test failure scenarios: API timeouts, invalid responses, network errors
- Factory pattern testing: provider creation with different configurations

@TestScenarios (Contract Verification):
- generate_structured_output: Mocked completion returns valid JSON, validates against Pydantic model
- generate_structured_output: Mocked completion returns invalid JSON, raises ValueError
- generate_text: Mocked completion returns expected string content
- Error handling: Mocked completion raises exception, propagates correctly
- Factory function: create_llm_provider returns configured instances
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, mock_open
from pydantic import BaseModel

from agent.infrastructure.llm.provider import LitellmProvider, create_llm_provider


# Test model for structured output validation
class TestStructuredModel(BaseModel):
    name: str
    value: int
    description: str


@pytest.mark.asyncio
class TestLitellmProvider:
    """Test suite for LitellmProvider implementation."""

    def test_provider_initialization_default(self):
        """Test provider initializes with default configuration."""
        provider = LitellmProvider()

        # Verify default model is set
        assert provider.default_model == "gemini/gemini-1.5-flash"
        # Timeout and retries should have sensible defaults
        assert provider.timeout == 60
        assert provider.max_retries == 3

    def test_provider_initialization_custom(self):
        """Test provider initializes with custom configuration."""
        provider = LitellmProvider(
            default_model="dashscope/qwen-max",
            api_key="test_key",
            api_base="https://custom.api.com",
            timeout=30,
            max_retries=2
        )

        assert provider.default_model == "dashscope/qwen-max"
        assert provider.api_key == "test_key"
        assert provider.api_base == "https://custom.api.com"
        assert provider.timeout == 30
        assert provider.max_retries == 2

    def test_provider_qwen_model_prefix(self):
        """Test that Qwen models get proper dashscope prefix."""
        provider = LitellmProvider(default_model="qwen-max")
        assert provider.default_model == "dashscope/qwen-max"

        # Already prefixed models should remain unchanged
        provider2 = LitellmProvider(default_model="dashscope/qwen-max")
        assert provider2.default_model == "dashscope/qwen-max"

    @patch('agent.infrastructure.llm.provider.os.getenv')
    def test_provider_api_key_from_env(self, mock_getenv):
        """Test API key loading from environment variables."""
        mock_getenv.return_value = "env_api_key"

        provider = LitellmProvider()  # No explicit api_key

        # Should use environment variable
        assert provider.api_key == "env_api_key"
        mock_getenv.assert_called_once_with('GEMINI_API_KEY')

    @patch('agent.infrastructure.llm.provider.completion')
    async def test_generate_structured_output_success(self, mock_completion):
        """Test successful structured output generation."""
        # Mock LLM response with valid JSON
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"name": "Test Item", "value": 42, "description": "A test item"}'
        mock_completion.return_value = mock_response

        provider = LitellmProvider()
        prompt = "Generate a test item with name, value, and description"
        result = await provider.generate_structured_output(prompt, TestStructuredModel)

        # Verify the result is properly validated
        assert isinstance(result, TestStructuredModel)
        assert result.name == "Test Item"
        assert result.value == 42
        assert result.description == "A test item"

        # Verify litellm was called with correct parameters
        mock_completion.assert_called_once()
        call_args = mock_completion.call_args[1]
        assert call_args['model'] == "gemini/gemini-1.5-flash"
        assert call_args['messages'][0]['content'] == prompt
        assert call_args['response_format'] == {"type": "json_object"}
        assert call_args['num_retries'] == 3

    @patch('agent.infrastructure.llm.provider.completion')
    async def test_generate_structured_output_invalid_json(self, mock_completion):
        """Test structured output generation with invalid JSON response."""
        # Mock LLM response with invalid JSON
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"name": "Test", invalid_json}'
        mock_completion.return_value = mock_response

        provider = LitellmProvider()
        prompt = "Generate invalid JSON"

        with pytest.raises(ValueError, match="Failed to generate structured output"):
            await provider.generate_structured_output(prompt, TestStructuredModel)

    @patch('agent.infrastructure.llm.provider.completion')
    async def test_generate_structured_output_empty_content(self, mock_completion):
        """Test structured output generation with empty response."""
        # Mock LLM response with empty content
        mock_response = MagicMock()
        mock_response.choices[0].message.content = ""
        mock_completion.return_value = mock_response

        provider = LitellmProvider()
        prompt = "Generate something"

        with pytest.raises(ValueError, match="Empty response from LLM"):
            await provider.generate_structured_output(prompt, TestStructuredModel)

    @patch('agent.infrastructure.llm.provider.completion')
    async def test_generate_structured_output_api_error(self, mock_completion):
        """Test structured output generation with API error."""
        # Mock litellm completion to raise an exception
        mock_completion.side_effect = Exception("API timeout")

        provider = LitellmProvider()
        prompt = "Generate content"

        with pytest.raises(ValueError, match="Failed to generate structured output"):
            await provider.generate_structured_output(prompt, TestStructuredModel)

    @patch('agent.infrastructure.llm.provider.completion')
    async def test_generate_text_success(self, mock_completion):
        """Test successful text generation."""
        # Mock LLM response with text content
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Generated text response"
        mock_completion.return_value = mock_response

        provider = LitellmProvider()
        prompt = "Generate some text"
        result = await provider.generate_text(prompt)

        assert result == "Generated text response"

        # Verify litellm call
        mock_completion.assert_called_once()
        call_args = mock_completion.call_args[1]
        assert call_args['messages'][0]['content'] == prompt

    @patch('agent.infrastructure.llm.provider.completion')
    async def test_generate_text_with_parameters(self, mock_completion):
        """Test text generation with custom parameters."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Custom response"
        mock_completion.return_value = mock_response

        provider = LitellmProvider()
        result = await provider.generate_text(
            "Test prompt",
            model_name="dashscope/qwen-max",
            temperature=0.5,
            max_tokens=100
        )

        assert result == "Custom response"

        # Verify parameters were passed correctly
        call_args = mock_completion.call_args[1]
        assert call_args['model'] == "dashscope/qwen-max"
        assert call_args['temperature'] == 0.5
        assert call_args['max_tokens'] == 100

    def test_get_provider_info(self):
        """Test provider info retrieval."""
        provider = LitellmProvider(
            default_model="test-model",
            api_key="test-key",
            api_base="https://test.com",
            timeout=45,
            max_retries=5
        )

        info = provider.get_provider_info()

        assert info['provider_name'] == 'litellm'
        assert info['default_model'] == 'test-model'
        assert info['has_api_key'] is True
        assert info['has_custom_base'] is True
        assert info['timeout'] == 45
        assert info['max_retries'] == 5


class TestCreateLLMProvider:
    """Test suite for factory function."""

    def test_create_gemini_provider(self):
        """Test creating Gemini provider."""
        provider = create_llm_provider("gemini")

        assert isinstance(provider, LitellmProvider)
        assert provider.default_model == "gemini/gemini-1.5-flash"

    def test_create_openai_provider(self):
        """Test creating OpenAI provider."""
        provider = create_llm_provider("openai")

        assert isinstance(provider, LitellmProvider)
        assert provider.default_model == "gpt-3.5-turbo"

    def test_create_anthropic_provider(self):
        """Test creating Anthropic provider."""
        provider = create_llm_provider("anthropic")

        assert isinstance(provider, LitellmProvider)
        assert provider.default_model == "claude-3-haiku-20240307"

    def test_create_dashscope_provider(self):
        """Test creating DashScope provider."""
        provider = create_llm_provider("dashscope")

        assert isinstance(provider, LitellmProvider)
        assert provider.default_model == "dashscope/qwen-max"

    def test_create_provider_custom_model(self):
        """Test creating provider with custom model."""
        provider = create_llm_provider("gemini", model_name="gemini/gemini-pro")

        assert isinstance(provider, LitellmProvider)
        assert provider.default_model == "gemini/gemini-pro"

    def test_create_provider_unknown_name(self):
        """Test creating provider with unknown name defaults to gemini."""
        provider = create_llm_provider("unknown")

        assert isinstance(provider, LitellmProvider)
        assert provider.default_model == "gemini/gemini-1.5-flash"

    def test_create_provider_with_kwargs(self):
        """Test creating provider with additional kwargs."""
        provider = create_llm_provider("gemini", api_key="custom-key", timeout=120)

        assert isinstance(provider, LitellmProvider)
        assert provider.api_key == "custom-key"
        assert provider.timeout == 120