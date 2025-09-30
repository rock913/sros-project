Feature: Multi-model support for embedding and generation

  Scenario: The agent can use different models for embedding and text generation
    Given the agent is configured with:
      | type              | model_name          |
      | embedding_model   | "siliconflow-model" |
      | generation_model  | "qwen-turbo"        |
    When the user asks "hello"
    Then the agent should respond using the "qwen-turbo" model for generation
