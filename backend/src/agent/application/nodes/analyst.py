"""
Analyst Node for Co-STORM Discourse Loop

This module implements the Analyst node that reads papers collected by Librarian
and synthesizes perspective summaries through LLM analysis.

@Co-STORM Algorithm:
Part of Sprint 2: From papers -> synthesize perspective summaries -> enable gap analysis
Each perspective gets a coherent summary combining insights from multiple papers.

@Hexagonal Architecture:
- Application layer: Orchestrates LLM calls via litellm_utils
- Uses domain prompts: ANALYST_PROMPT for structured synthesis
- State Updates: Populates node.summary for each mindmap perspective
"""

from typing import List

from agent.domain.prompts.costorm import ANALYST_PROMPT
from agent.domain.schemas.paper import Paper
from agent.application.nodes.costorm import CoStormState


def analyst_node(state: CoStormState) -> CoStormState:
    """Analyze papers from each perspective and generate LLM summaries.

    For each mindmap node with papers but no summary, calls LLM to synthesize
    a coherent perspective summary combining insights from all papers in that node.

    @TestScenarios
    - mindmap.nodes with papers and empty summary -> generates LLM summaries
    - nodes without papers -> skipped gracefully
    - LLM errors -> sets fallback "unable to synthesize" message

    Args:
        state: Co-STORM state with populated documents and mindmap

    Returns:
        Updated state with node.summary populated via LLM synthesis
    """
    print("---CO-STORM NODE: analyst---")

    if not state.get("mindmap"):
        print("WARNING: No mindmap in state, analyst has nothing to analyze")
        return state

    mindmap = state["mindmap"]

    for node in mindmap.nodes:
        if node.papers and not node.summary:  # Has papers but no summary yet
            print(f"Analyzing papers for node '{node.id}': {len(node.papers)} papers")

            try:
                # Format papers for LLM context
                papers_data = [paper.model_dump() for paper in node.papers]
                papers_json = str(papers_data)

                # Use domain prompt for structured synthesis
                prompt = ANALYST_PROMPT.format(
                    papers_json=papers_json,
                    perspective_name=node.name
                )

                # Application layer calls infrastructure via litellm
                from litellm import completion
                from agent.configuration import Configuration

                config = {}
                cfg = Configuration.from_runnable_config(config)

                # Fix for DashScope model prefix
                model = cfg.generation_model
                if (cfg.generation_llm_provider == "dashscope" or "qwen" in model.lower()) and not model.startswith("dashscope/"):
                    model = f"dashscope/{model}"

                # LLM call for synthesis (structured text output)
                response = completion(
                    model=model,
                    messages=[{"content": prompt, "role": "user"}],
                    num_retries=2,
                    api_key=cfg.generation_api_key or None,
                    base_url=cfg.generation_api_base or None,
                )

                summary = response.choices[0].message.content.strip()
                node.summary = summary  # Update node in-place

                print(f"✓ Generated {len(summary)} char summary for '{node.id}'")

            except Exception as e:
                print(f"ERROR: Failed to analyze '{node.id}': {e}")
                # Fallback message allows workflow continuation
                node.summary = f"Unable to synthesize summary for {node.name}: {str(e)}"

    print("✓ Analyst completed: perspective summaries generated")
    return state