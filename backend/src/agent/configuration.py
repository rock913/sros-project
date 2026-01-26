import os
from typing import Any

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field


class Configuration(BaseModel):
    """The configuration for the agent."""

    embedding_model: str = Field(
        default="Qwen/Qwen3-Embedding-8B",
        metadata={
            "description": "The name of the embedding model to use."
        },
    )

    embedding_api_base: str = Field(
        default="https://api.siliconflow.cn/v1",
        metadata={
            "description": "The API base URL for the embedding model."
        },
    )

    embedding_api_key: str = Field(
        default_factory=lambda: os.environ.get("SILICONFLOW_API_KEY", ""),
        metadata={
            "description": "The API key for the embedding model."
        },
    )

    embedding_llm_provider: str = Field(
        default="openai",
        metadata={
            "description": "The litellm provider for the embedding model. Defaults to 'openai' for OpenAI-compatible APIs like SiliconFlow."
        },
    )
    
    generation_llm_provider: str = Field(
        default="openai",
        metadata={
            "description": "The litellm provider for generation tasks (DashScope Qwen via OpenAI-compatible API by default)."
        },
    )

    embedding_dimensions: int = Field(
        default=2048,
        metadata={
            "description": "The dimensionality for embedding vectors when calling SiliconFlow embeddings API."
        },
    )

    generation_model: str = Field(
        default="qwen-max",
        metadata={
            "description": "The name of the language model to use for generation tasks (query generation, reflection, and final answer)."
        },
    )

    number_of_initial_queries: int = Field(
        default=3,
        metadata={"description": "The number of initial search queries to generate."},
    )

    max_research_loops: int = Field(
        default=2,
        metadata={"description": "The maximum number of research loops to perform."},
    )

    # NOTE: A duplicate field (generation_llm_provider) previously overwrote the intended default
    # and forced 'vertex_ai', causing credential lookup failures when ADC was not configured.
    # That duplicate has been removed. To force Vertex AI explicitly, set env GENERATION_LLM_PROVIDER=vertex_ai.

    @classmethod
    def from_runnable_config(
        cls, config: Union[RunnableConfig, dict, None] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        if LANGCHAIN_AVAILABLE:
            configurable = (
                config["configurable"] if config and "configurable" in config else {}
            )
        else:
            configurable = {}

        # Get raw values from environment or config
        raw_values: dict[str, Any] = {
            name: os.environ.get(name.upper(), configurable.get(name))
            for name in cls.model_fields.keys()
        }

        # Filter out None values
        values = {k: v for k, v in raw_values.items() if v is not None}

        inst = cls(**values)

        # 修复逻辑：如果模型是 qwen 系列，强制使用 openai provider (DashScope 兼容)
        if "qwen" in inst.generation_model.lower() and inst.generation_llm_provider != "openai":
            inst.generation_llm_provider = "openai"

        # Automatic fallback: if provider is vertex_ai but no ADC credentials are present, and a GEMINI_API_KEY
        # is supplied, switch to gemini provider to avoid 500 errors.
        if (
            inst.generation_llm_provider == "vertex_ai"
            and not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            and os.environ.get("GEMINI_API_KEY")
        ):
            inst.generation_llm_provider = "gemini"
        return inst
