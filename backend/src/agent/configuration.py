import os
from pydantic import BaseModel, Field
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig


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
        default="gemini",
        metadata={
            "description": "The litellm provider for generation tasks (e.g., gemini studio models)."
        },
    )

    embedding_dimensions: int = Field(
        default=2048,
        metadata={
            "description": "The dimensionality for embedding vectors when calling SiliconFlow embeddings API."
        },
    )

    generation_model: str = Field(
        default="gemini/gemini-1.5-flash",
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

    generation_llm_provider: str = Field(
        default="vertex_ai",
        metadata={
            "description": "The litellm provider for the generation model. Defaults to 'vertex_ai' for Google Vertex AI models."
        },
    )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )

        # Get raw values from environment or config
        raw_values: dict[str, Any] = {
            name: os.environ.get(name.upper(), configurable.get(name))
            for name in cls.model_fields.keys()
        }

        # Filter out None values
        values = {k: v for k, v in raw_values.items() if v is not None}

        return cls(**values)
