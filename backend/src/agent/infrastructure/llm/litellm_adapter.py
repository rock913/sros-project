"""LiteLLMAdapter: An adapter for interacting with LiteLLM.
"""

from typing import Any, List, Type, Union

from litellm import completion
from pydantic import BaseModel

from agent.domain.ports.llm import LanguageModel, LLMResponse


class LiteLLMAdapter(LanguageModel):
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-4", 
        response_format: Type[BaseModel] | None = None,
        tools: List[Dict[str, Any]] | None = None
    ) -> Union[LLMResponse, BaseModel, Any]:
        try:
            response = completion(
                model=model,
                messages=messages,
                tools=tools if tools else []
            )
            content = response['choices'][0]['message']['content']
            
            if response_format:
                return response_format.parse_raw(content)
            
            tool_calls = response['choices'][0]['message'].get('tool_calls', [])
            return LLMResponse(content=content, tool_calls=tool_calls)
        
        except Exception as e:
            # Handle LiteLLM exceptions and wrap in domain exceptions if needed
            raise Exception(f"LiteLLM Error: {str(e)}")
