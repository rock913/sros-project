Feature: Agent's Optimal Academic Research Workflow

  As a user, I want the agent to follow the defined "plan-execute-reflect" loop to conduct thorough research, refining its searches until the question is fully answered.

  Scenario: User asks a question that requires research refinement
    Given the agent server is running
    When the user asks "What is the impact of AI on climate change?"

    # 1. Initial Plan and Search
    Then the agent's response stream should show it is "generating an initial research plan"
    And the agent should first call tools like "ArxivQueryRun" or "PubmedQueryRun" with broad queries such as "AI and climate change"

    # 2. Reflection and Loop
    And the agent's response stream should show it is "reflecting on the initial results" and identifying knowledge gaps
    And the agent's response stream should show it is "formulating follow-up queries" to get more specific information, such as "AI for carbon capture"
    And the agent should then call "ArxivQueryRun" or "PubmedQueryRun" a second time with these refined queries

    # 3. Final Report
    And after finding sufficient information, the agent should finally deliver a structured "report" that synthesizes all findings and includes citations