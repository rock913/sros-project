"""
LLM Provider Infrastructure Implementation

This module provides concrete implementations of the LLMProviderPort,
wrapping various LLM APIs through the Litellm library for unified access.

@Hexagonal Architecture:
- Infrastructure Layer: External API integrations and I/O operations
- Factory Pattern: Runtime provider selection and configuration
- Litellm Abstraction: Unified interface across multiple LLM providers

@Infrastructure Responsibilities:
- API key management and provider authentication
- Model selection and parameter optimization
- Error handling with retry logic and fallbacks
- Cost tracking and usage monitoring
- Provider-specific configurations (timeouts, rate limits)

@Supported Providers:
- OpenAI (GPT models)
- Google (Gemini models)
- Anthropic (Claude models)
- DashScope (Qwen models)
- And other Litellm-supported providers
"""

import os
from typing import Any, Dict, Optional, Type, TypeVar

from litellm import completion
from pydantic import BaseModel

from agent.domain.ports.llm_provider import LLMProviderPort

# Type variable matching the port
T = TypeVar('T', bound=BaseModel)


class LitellmProvider(LLMProviderPort):
    """Concrete LLM provider implementation using Litellm.

    This adapter provides unified access to multiple LLM providers through
    the Litellm library, implementing the domain contract for structured output generation.
    """

    def __init__(
        self,
        default_model: str = "gemini/gemini-1.5-flash",
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        timeout: int = 60,
        max_retries: int = 3
    ):
        """Initialize the LLM provider with configuration.

        Args:
            default_model: Default model to use for completions
            api_key: API key for the LLM provider
            api_base: Custom API base URL (for local/self-hosted models)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.default_model = default_model
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.api_base = api_base
        self.timeout = timeout
        self.max_retries = max_retries

        # Ensure Qwen models have proper prefix
        if self.default_model.startswith("qwen") and not self.default_model.startswith("dashscope/"):
            self.default_model = f"dashscope/{self.default_model}"

    async def generate_structured_output(
        self,
        prompt: str,
        output_model: Type[T],
        *,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> T:
        """Generate structured output using LLM with JSON mode.

        Uses Litellm's json_object response format for structured generation,
        then validates the result against the provided Pydantic model.

        Args:
            prompt: Natural language prompt for the LLM
            output_model: Pydantic model class for validation
            model_name: Optional model override
            temperature: Generation temperature (0.0-1.0)
            max_tokens: Maximum output tokens
            **kwargs: Additional Litellm parameters

        Returns:
            Validated instance of the output model

        Raises:
            ValueError: If the LLM response cannot be parsed or validated
            Exception: For network/API errors after retries
        """
        model = model_name or self.default_model

        # Prepare request parameters
        request_params = {
            "model": model,
            "messages": [{"content": prompt, "role": "user"}],
            "response_format": {"type": "json_object"},
            "temperature": temperature,
            "num_retries": self.max_retries,
        }

        # Add optional parameters
        if max_tokens is not None:
            request_params["max_tokens"] = max_tokens

        # Add API credentials if available
        if self.api_key:
            request_params["api_key"] = self.api_key
        if self.api_base:
            request_params["base_url"] = self.api_base

        # Add any additional kwargs
        request_params.update(kwargs)

        try:
            # Call Litellm completion API
            response = completion(**request_params)

            # Extract and parse JSON response
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from LLM")

            # Pydantic validation ensures domain contract compliance
            # This will raise ValidationError if the response doesn't match the schema
            return output_model.model_validate_json(content)

        except Exception as e:
            # Log error details for debugging
            error_msg = f"LLM generation failed for model {model}: {str(e)}"
            print(f"[LLM Provider] {error_msg}")

            # For structured output, we cannot provide meaningful fallbacks
            # The domain layer should handle this with appropriate error recovery
            raise ValueError(f"Failed to generate structured output: {error_msg}") from e

    async def generate_text(
        self,
        prompt: str,
        *,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        """Generate free-form text using LLM.

        Args:
            prompt: Natural language prompt for text generation
            model_name: Optional model override
            temperature: Generation temperature
            max_tokens: Maximum output tokens
            **kwargs: Additional Litellm parameters

        Returns:
            Generated text content

        Raises:
            Exception: For network/API errors after retries
        """
        model = model_name or self.default_model

        request_params = {
            "model": model,
            "messages": [{"content": prompt, "role": "user"}],
            "temperature": temperature,
            "num_retries": self.max_retries,
        }

        if max_tokens is not None:
            request_params["max_tokens"] = max_tokens

        if self.api_key:
            request_params["api_key"] = self.api_key
        if self.api_base:
            request_params["base_url"] = self.api_base

        request_params.update(kwargs)

        try:
            response = completion(**request_params)
            content = response.choices[0].message.content or ""
            return content.strip()

        except Exception as e:
            error_msg = f"Text generation failed for model {model}: {str(e)}"
            print(f"[LLM Provider] {error_msg}")
            raise Exception(error_msg) from e

    def get_provider_info(self) -> Dict[str, Any]:
        """Get provider configuration information."""
        return {
            "provider_name": "litellm",
            "default_model": self.default_model,
            "has_api_key": bool(self.api_key),
            "has_custom_base": bool(self.api_base),
            "timeout": self.timeout,
            "max_retries": self.max_retries,
        }


# Factory function for provider instantiation
def create_llm_provider(
    provider_name: str = "gemini",
    model_name: Optional[str] = None,
    **kwargs: Any
) -> LLMProviderPort:
    """Factory function to create LLM provider instances.

    Args:
        provider_name: Name of the provider ('openai', 'gemini', 'anthropic', etc.)
        model_name: Specific model name to use
        **kwargs: Additional configuration parameters

    Returns:
        Configured LLM provider instance

    @Factory Pattern:
    - Centralizes provider creation logic
    - Handles provider-specific configurations
    - Enables runtime provider switching
    """
    if provider_name == "gemini":
        default_model = model_name or "gemini/gemini-1.5-flash"
    elif provider_name == "openai":
        default_model = model_name or "gpt-3.5-turbo"
    elif provider_name == "anthropic":
        default_model = model_name or "claude-3-haiku-20240307"
    elif provider_name == "dashscope":
        default_model = model_name or "dashscope/qwen-max"
    else:
        # Fallback to direct model specification
        default_model = model_name or "gemini/gemini-1.5-flash"

    return LitellmProvider(
        default_model=default_model,
        **kwargs
    )