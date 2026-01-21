"""
LiteLLMAdapter: An adapter for interacting with LiteLLM.
"""

from typing import Any, List, Optional, Type, Union
from pydantic import BaseModel
from litellm import completion
from agent.domain.ports.llm import LLMResponse, LanguageModel

class LiteLLMAdapter(LanguageModel):
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-4", 
        response_format: Optional[Type[BaseModel]] = None,
        tools: Optional[List[Dict[str, Any]]] = None
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
