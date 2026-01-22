"""
Test cases for LiteLLMAdapter.
"""

import unittest
from unittest.mock import patch

from pydantic import BaseModel

from agent.domain.ports.llm import LLMResponse
from agent.infrastructure.llm.litellm_adapter import LiteLLMAdapter


class TestLiteLLMAdapter(unittest.TestCase):

    @patch('agent.infrastructure.llm.litellm_adapter.completion')
    def test_simple_text_response(self, mock_completion):
        mock_completion.return_value = {
            'choices': [{'message': {'content': 'Hello world'}}]
        }
        adapter = LiteLLMAdapter()
        response = adapter.generate(messages=[{'role': 'user', 'content': 'Say hello'}])
        self.assertIsInstance(response, LLMResponse)
        self.assertEqual(response.content, 'Hello world')
        self.assertEqual(response.tool_calls, [])

    @patch('agent.infrastructure.llm.litellm_adapter.completion')
    def test_structured_output(self, mock_completion):
        class MyModel(BaseModel):
            value: int
    
        mock_completion.return_value = {
            'choices': [{'message': {'content': '{"value": 42}'}}]
        }
        adapter = LiteLLMAdapter()
        response = adapter.generate(messages=[{'role': 'user', 'content': 'Return a number'}], response_format=MyModel)
        self.assertIsInstance(response, MyModel)
        self.assertEqual(response.value, 42)

    @patch('agent.infrastructure.llm.litellm_adapter.completion')
    def test_error_handling(self, mock_completion):
        mock_completion.side_effect = Exception("API Error")
        adapter = LiteLLMAdapter()
        with self.assertRaises(Exception) as context:
            adapter.generate(messages=[{'role': 'user', 'content': 'Say hello'}])
        self.assertIn("LiteLLM Error", str(context.exception))

if __name__ == '__main__':
    unittest.main()
