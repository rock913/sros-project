import argparse
import asyncio
from langgraph_sdk import RemoteRunnable

async def main():
    """
    Connects to the backend agent service and streams its final output
    for a given research topic.
    """
    parser = argparse.ArgumentParser(
        description="Run a research task with the backend agent and stream the output."
    )
    parser.add_argument(
        "topic",
        type=str,
        help="The research topic for the agent to investigate.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=2024, # Default port from docker-compose-dev.yml
        help="The port of the backend service.",
    )
    args = parser.parse_args()

    # The `langgraph dev` command serves the graph from the `agent.graph` module.
    # By default, it's exposed at an endpoint named after the module.
    agent_url = f"http://localhost:{args.port}/agent"

    print(f"--- Connecting to agent at: {agent_url} ---")
    agent = RemoteRunnable(agent_url)

    print(f"--- Starting research task for topic: '{args.topic}' ---")
    
    # The input to the graph is a dictionary with a "messages" key
    input_data = {"messages": [{"role": "user", "content": args.topic}]}

    print("\n--- Agent Output Stream ---")
    final_state = {}
    async for chunk in agent.astream(input_data):
        final_state.update(chunk)
        # Print out the keys as they stream in to show progress
        print(f"Received chunk with keys: {list(chunk.keys())}")

    print("\n--- Research Task Finished ---")
    
    report = final_state.get("report", "No report was generated.")
    
    print("\n--- Final Report ---")
    print(report)


if __name__ == "__main__":
    # To run this script, the backend service must be running.
    # You can start it with: `docker-compose -f docker-compose-dev.yml up -d`
    # Then run this script from your terminal within the `backend` directory:
    # `uv run python examples/e2e_test_case.py "The impact of AI on climate change"`
    asyncio.run(main())
