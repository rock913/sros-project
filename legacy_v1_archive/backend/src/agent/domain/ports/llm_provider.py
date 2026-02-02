"""
LLM Provider Port (Protocol) for Hexagonal Architecture

This module defines the abstract interface for Large Language Model interactions,
enabling infrastructure abstraction and dependency injection throughout the research platform.

@Hexagonal Architecture:
- Domain Layer: Pure abstract contracts (no I/O, no implementations)
- Application Layer: Uses LLM provider contracts for AI-powered logic
- Infrastructure Layer: Provides concrete implementations (litellm adapters, API clients, etc.)

@TestScenarios (verified by unittest.mock at infrastructure layer)
- generate_structured_output: Converts natural language prompt to structured domain model
- Handles various LLM providers through unified interface
- Supports different output formats (JSON, Pydantic models)
- Graceful error handling with fallbacks
- Cost tracking and usage monitoring
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, TypeVar

# Type variable for structured output models
T = TypeVar('T', bound=object)


class LLMProviderPort(ABC):
    """Abstract base class defining the LLM provider contract.

    This protocol ensures all LLM provider implementations provide
    consistent AI-powered capabilities for the research platform.

    The core abstraction is `generate_structured_output()` which handles:
    - Prompt formatting and model selection
    - Structured output parsing (JSON/Pydantic)
    - Error handling and retries
    - Provider-specific optimizations

    @Contract Requirements:
    - Must support asynchronous operations for non-blocking workflows
    - Must handle provider-specific configuration (API keys, models, timeouts)
    - Must provide consistent error handling across providers
    - Must support structured output validation via domain schemas

    @Implementation Notes:
    - Concrete implementations will wrap various LLM APIs (OpenAI, Anthropic, Google, etc.)
    - Factory pattern enables runtime provider selection (dev/prod environments)
    - Single-responsibility: Only LLM interaction duties, no business logic
    """

    @abstractmethod
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
        """Generate structured output from LLM using natural language prompt.

        This is the primary method for AI-powered structured generation,
        such as converting research topics into knowledge maps, or synthesizing
        content into domain models.

        Args:
            prompt: Natural language prompt describing the desired output
            output_model: Pydantic model class defining the expected structure
            model_name: Optional model override (defaults to configured model)
            temperature: Creativity/randomness parameter (0.0-1.0)
            max_tokens: Maximum output length limit
            **kwargs: Additional provider-specific parameters

        Returns:
            Validated instance of the output_model with generated content

        @TestScenarios
        - Valid prompt returns correctly validated model instance
        - Invalid prompt raises validation error (not raw API error)
        - Model fallback on provider failures
        - Timeout handling and retry logic
        - Cost tracking for usage monitoring
        """
        pass

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        *,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        """Generate free-form text output from LLM.

        For cases where structured output is not required, this method
        provides raw text generation capabilities.

        Args:
            prompt: Natural language prompt for text generation
            model_name: Optional model override
            temperature: Creativity parameter
            max_tokens: Maximum output length
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text content as string

        @TestScenarios
        - Valid prompt returns coherent text
        - Empty/invalid prompt handled gracefully
        - Token limits respected
        - Unicode and formatting preserved
        """
        pass

    @abstractmethod
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the current provider configuration.

        Useful for debugging, cost tracking, and provider-specific optimizations.

        Returns:
            Dictionary containing provider metadata (name, model, capabilities, etc.)

        @TestScenarios
        - Returns correct provider identification
        - Includes model and configuration details
        - Used for conditional logic in application layer
        """
        pass