from typing import Any, Dict, List, Optional, Protocol, Union
from pydantic import BaseModel, ConfigDict

class LLMResponse(BaseModel):
    content: str
    tool_calls: List[Dict[str, Any]] = []
    
    model_config = ConfigDict(extra='ignore')

class LanguageModel(Protocol):
    """
    Protocol for Large Language Model interactions.
    
    @TestScenarios
    1. Completion:
       - Input: List of messages (system/user).
       - Expected: Returns LLMResponse with content.
       
    2. Structured Output:
       - Input: Pydantic model class as response_format.
       - Expected: Returns valid instance of the Pydantic model.
       
    3. Tool Calling:
       - Input: Tools definition in request.
       - Expected: Returns LLMResponse with tool_calls populated if model decides to use tool.
    """
    
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-4o", 
        response_format: Optional[type[BaseModel]] = None,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Union[LLMResponse, BaseModel, Any]:
        """Generate a response from the LLM."""
