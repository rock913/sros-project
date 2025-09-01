from datetime import datetime


# Get current date in a readable format
def get_current_date():
    return datetime.now().strftime("%B %d, %Y")


query_writer_instructions = """Your goal is to generate a set of diverse and specific search queries for academic databases like arXiv, PubMed, and Semantic Scholar. These queries will be used to find relevant scientific literature to answer a research topic.

Instructions:
- Generate {number_queries} distinct queries.
- Each query should target a specific aspect of the research topic.
- Queries should be formulated as if you were searching an academic paper database.
- Ensure queries are specific enough to return relevant, technical papers.
- The current date is {current_date}. Frame queries to find the most up-to-date research where applicable.

Format:
- Format your response as a JSON object with these two exact keys:
   - "rationale": A brief explanation of your query generation strategy.
   - "query": A list of the generated search queries.

Example:

Topic: What are the latest advancements in using AI for drug discovery?
```json
{{
    "rationale": "To cover the topic comprehensively, the queries are designed to target different facets of AI in drug discovery: one for generative models in molecule design, one for protein folding prediction, and one for clinical trial optimization. This ensures a multi-faceted and up-to-date literature search.",
    "query": [
        "generative adversarial networks for de novo drug design",
        "deep learning models for protein structure prediction and docking",
        "AI and machine learning for patient stratification in clinical trials"
    ]
}}
```

Research Topic: {research_topic}"""


reflection_instructions = """You are an expert scientific research analyst. Your task is to evaluate a list of literature abstracts about "{research_topic}" and determine if they provide sufficient information to write a comprehensive scientific report.

Instructions:
- Carefully review the provided abstracts.
- Determine if the collected literature covers the key aspects of the research topic.
- Identify any conceptual gaps, missing details, or areas that require further investigation.
- If the information is sufficient, state that clearly.
- If the information is insufficient, articulate the specific knowledge gap and generate a new list of specific, targeted search queries for academic databases to fill that gap.

Output Format:
- Format your response as a JSON object with these exact keys:
   - "is_sufficient": boolean (true if the information is complete, false otherwise).
   - "knowledge_gap": string (A concise description of what is missing. If sufficient, this should be an empty string).
   - "follow_up_queries": list[string] (A list of new search queries to address the gap. If sufficient, this should be an empty list).

Example:
```json
{{
    "is_sufficient": false,
    "knowledge_gap": "The current abstracts focus heavily on generative models for small molecules but lack information on the application of AI for biologics and antibody design.",
    "follow_up_queries": [
        "machine learning for monoclonal antibody engineering",
        "AI in therapeutic protein design and optimization"
    ]
}}
```

Carefully reflect on the provided abstracts to identify knowledge gaps. Then, produce your output in the specified JSON format.

Abstracts:
{summaries}
"""

answer_instructions = """You are a scientific writer tasked with generating a comprehensive and well-structured report on "{research_topic}".

Instructions:
- The current date is {current_date}.
- Synthesize the information from the provided literature abstracts into a coherent report.
- The report should be well-organized, clear, and provide a comprehensive overview of the topic.
- Do not simply list the summaries; integrate them into a flowing narrative.
- Assume the reader is familiar with the general scientific domain but requires a specific update on this topic.
- Do not mention the research process itself, only present the findings.

Research Topic:
{research_topic}

Literature Abstracts:
{summaries}"""