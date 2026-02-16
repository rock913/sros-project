import os

def test_environment_variables(monkeypatch):
    """Test that environment variables are handled correctly."""
    # Test default values
    assert "PATH" in os.environ  # Basic sanity check
    
    # Test setting and getting environment variables
    test_var = "TEST_SROS_VAR"
    test_value = "test_value"

    monkeypatch.setenv(test_var, test_value)
    assert os.environ[test_var] == test_value