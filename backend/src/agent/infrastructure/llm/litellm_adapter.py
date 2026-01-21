from typing import Any, List, Optional, Type, Union
from pydantic import BaseModel
from litellm import completion
from agent.domain.ports.llm import LLMResponse, LanguageModel
