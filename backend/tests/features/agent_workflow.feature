Feature: Agent's Optimal Academic Research Workflow

  As a user, I want the agent to follow the defined "plan-execute-reflect" loop to conduct thorough research, refining its searches until the question is fully answered.

  Scenario: User asks a question that requires research refinement
    Given the agent server is running
    And the agent is configured for the 'Research Refinement' scenario with research topic 'AI and climate change'
    When the user asks "What is the impact of AI on climate change?"

    # 1. Initial Plan and Search
    Then the agent's response stream should show it is "generating an initial research plan"
    And the agent should first call tools like "ArxivQueryRun" or "PubmedQueryRun" with broad queries such as "AI and climate change"

    # 2. Reflection and Loop
    And the agent's response stream should show it is "reflecting on the initial results"
    And the agent's response stream should show it is "formulating follow-up queries"
    And the agent should then call "ArxivQueryRun" or "PubmedQueryRun" a second time with these refined queries

    # 3. Final Report
    And after finding sufficient information, the agent should finally deliver a structured "report" that synthesizes all findings and includes citations

  Scenario: Research with No Further Refinement Needed
    Given the agent server is running
    And the agent is configured for the 'No Refinement Needed' scenario with research topic 'What is the capital of France?'
    When the user asks "What is the capital of France?"
    Then the agent should generate initial search queries
    And the agent should execute searches using tools like "ArxivQueryRun"
    And the agent should reflect on the initial search results
    And the agent should find sufficient information without generating follow-up queries
    And the agent should manage resources by finding DOIs and adding PDFs to Zotero (even if none are found)
    And the agent should synthesize knowledge from full-text documents (even if none are processed)
    And the agent should generate a comprehensive report
    And the final report should be delivered to the user

  Scenario: Research with Max Loop Reached
    Given the agent server is running
    And the agent is configured for the 'Max Loop Reached' scenario with research topic 'A very obscure and hard to research topic'
    And the maximum research loops is set to 1
    When the user asks "A very obscure and hard to research topic"
    Then the agent should generate initial search queries
    And the agent should execute searches using tools like "ArxivQueryRun"
    And the agent should reflect on the initial search results
    And the agent should identify knowledge gaps and generate follow-up queries
    And the agent should execute refined searches
    And the agent should reach the maximum research loops
    And the agent should proceed to manage resources despite insufficient information
    And the agent should synthesize knowledge from full-text documents (even if limited)
    And the agent should generate a report based on available information
    And the final report should be delivered to the user

  Scenario: Resource Management and RAG Integration
    Given the agent server is running
    And the agent is configured for the 'Resource Management and RAG' scenario with research topic 'Papers on quantum entanglement'
    When the user asks "Find papers on quantum entanglement and summarize them"
    Then the agent should generate initial search queries
    And the agent should execute searches using tools like "ArxivQueryRun"
    And the agent should find abstracts containing DOIs
    And the agent should use "unpaywall_tool" to find PDF URLs
    And the agent should use "zotero_tool" to add papers to Zotero
    And the agent should download and process full-text PDFs
    And the agent should chunk and embed the PDF content into the vector database
    And the agent should synthesize knowledge from the vector database
    And the agent should generate a comprehensive report with citations
    And the final report should be delivered to the user
