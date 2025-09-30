import pytest
from pytest_bdd import given, parsers
from unittest.mock import patch, MagicMock

from agent.configuration import Configuration

@given(parsers.parse('the agent is configured with:\n{config_table}'), target_fixture='configured_agent_context')
def configure_agent_with_models(config_table):
    """Configures the agent with specified embedding and generation models."""
    # Split the table into lines, skip the header, and parse the rows
    config_lines = [line.strip().split('|') for line in config_table.strip().split('\n') if line.strip()]
    # Skip header row by starting from the second line
    config = {line[1].strip(): line[2].strip().strip('"') for line in config_lines[1:]}

    # Patch the Configuration class to use these models
    with patch.object(Configuration, 'from_runnable_config') as mock_from_config:
        mock_config = MagicMock()
        mock_config.generation_model = config.get('generation_model')
        mock_config.embedding_model = config.get('embedding_model')
        # Add other necessary attributes from Configuration
        mock_config.number_of_initial_queries = 3
        mock_from_config.return_value = mock_config

        context = {
            "generation_model": config.get('generation_model'),
            "embedding_model": config.get('embedding_model'),
        }
        yield context
