import os
import unittest
from unittest.mock import MagicMock, patch

from agent.langfuse_manager import LangfuseManager, NoOpTrace

class TestLangfuseManagerCompat(unittest.TestCase):
    def setUp(self):
        # Reset singleton
        LangfuseManager._instance = None
        LangfuseManager._enabled = False
        
    @patch('agent.langfuse_manager.Langfuse')
    def test_trace_compatibility_v3(self, MockLangfuse):
        """Test compatibility with SDK v3 where trace() is missing but start_span() exists."""
        # Setup mock instance
        mock_instance = MockLangfuse.return_value
        # Ensure trace method does NOT exist
        del mock_instance.trace 
        
        # Ensure start_span exists and returns a mock span
        mock_span = MagicMock()
        mock_instance.start_span.return_value = mock_span
        
        # Initialize
        os.environ["LANGFUSE_PUBLIC_KEY"] = "pk"
        os.environ["LANGFUSE_SECRET_KEY"] = "sk"
        LangfuseManager.initialize()
        
        # Call trace
        t = LangfuseManager.trace(name="test-trace", user_id="user-123", metadata={"a": 1})
        
        # Assertions
        # 1. start_span called with name and metadata (if passed)
        mock_instance.start_span.assert_called()
        call_kwargs = mock_instance.start_span.call_args.kwargs
        self.assertEqual(call_kwargs.get('name'), "test-trace")
        self.assertEqual(call_kwargs.get('metadata'), {"a": 1})
        self.assertNotIn('user_id', call_kwargs)
        
        # 2. trace object is the span
        self.assertEqual(t, mock_span)
        
        # 3. update called with user_id
        mock_span.update.assert_called_with(user_id="user-123")
        
        print("✅ Test passed: LangfuseManager handles v3 SDK correctly")

if __name__ == '__main__':
    unittest.main()
