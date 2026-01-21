"""BDD step definitions for multi-model support scenario.

This file was cleaned up to remove duplicated / corrupted code blocks that
prevented pytest-bdd from registering the steps (leading to StepDefinitionNotFound).

Responsibilities here:
 - Provide a single scenario binding the feature file.
 - Implement a robust Given step that parses the Gherkin table.
 - Patch Configuration.from_runnable_config to inject test models.
 - Re-use existing global patches provided by conftest (avoid double patching completion/embeddings).
 - Verify that the litellm completion call receives the expected model name.
"""

import asyncio
import pathlib

from langchain_core.messages import HumanMessage
from pytest_bdd import given, parsers, scenario, then, when

from agent.configuration import Configuration
from agent.application.workflows.research_workflow import graph


@scenario('../features/multi_model_support.feature', 'The agent can use different models for embedding and text generation')
def test_multi_model_support_scenario():
    pass


@given("the agent is configured with:", target_fixture='configured_agent_context')
def configure_models(monkeypatch, agent_test_context):
    """Robust table parsing by reading the feature file directly.

    Avoids fragile regex binding; ensures stability even if whitespace changes.
    """
    feature_path = pathlib.Path(__file__).parent.parent / 'features' / 'multi_model_support.feature'
    content = feature_path.read_text(encoding='utf-8').splitlines()
    # Locate the Given line verbatim
    try:
        idx = next(i for i, l in enumerate(content) if l.strip() == 'Given the agent is configured with:')
    except StopIteration:  # Should not happen unless feature modified
        raise AssertionError('Given step line not found in feature file')
    table_lines = []
    for line in content[idx+1:]:
        if line.strip().startswith('|'):
            table_lines.append(line)
        elif line.strip() == '':
            continue
        else:
            break
    if not table_lines:
        raise AssertionError('No table lines found after Given step')
    header = [h.strip() for h in table_lines[0].strip('|').split('|') if h.strip()]
    models = {}
    for row_line in table_lines[1:]:
        cells = [c.strip().strip('"') for c in row_line.strip('|').split('|') if c.strip()]
        row = dict(zip(header, cells))
        mtype = row.get('type')
        mname = row.get('model_name')
        if mtype and mname:
            models[mtype] = mname
    if not models:
        raise AssertionError('Parsed zero model rows from table')

    original_from = Configuration.from_runnable_config
    def _patched_from(cfg):
        c = original_from(cfg)
        if models.get('generation_model'):
            c.generation_model = models['generation_model']
        if models.get('embedding_model'):
            c.embedding_model = models['embedding_model']
        return c
    monkeypatch.setattr(Configuration, 'from_runnable_config', staticmethod(_patched_from))
    agent_test_context['models'] = models
    return agent_test_context


@when(parsers.parse('the user asks "{question}"'))
def user_asks_question(configured_agent_context, question):
    # We rely on the existing patched completion mock from conftest
    initial_state = {"messages": [HumanMessage(content=question)]}
    try:
        asyncio.run(graph.ainvoke(initial_state, config={}))
    except Exception:
        # The whole graph isn't fully mocked; early failure is acceptable as long as completion was invoked.
        pass
    return configured_agent_context


@then(parsers.parse('the agent should respond using the "{model_name}" model for generation'))
def assert_generation_model_used(configured_agent_context, model_name):
    mock_completion = configured_agent_context['mock_completion']
    assert mock_completion.called, 'Expected litellm.completion to be called at least once'
    # Inspect the first call kwargs
    _, first_kwargs = mock_completion.call_args
    used_model = first_kwargs.get('model')
    assert used_model == model_name, f"Expected model '{model_name}' but got '{used_model}'"
