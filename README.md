# Gemini Fullstack LangGraph Quickstart

This project demonstrates a fullstack application using a React frontend and a LangGraph-powered backend agent. The agent is designed to perform comprehensive research on a user's query by dynamically generating search terms, querying the web using Google Search, reflecting on the results to identify knowledge gaps, and iteratively refining its search until it can provide a well-supported answer with citations. This application serves as an example of building research-augmented conversational AI using LangGraph and Google's Gemini models.

<img src="./app.png" title="Gemini Fullstack LangGraph" alt="Gemini Fullstack LangGraph" width="90%">

## Features

- 💬 Fullstack application with a React frontend and LangGraph backend.
- 🧠 Powered by a LangGraph agent for advanced research and conversational AI.
- 🔍 Dynamic search query generation using Google Gemini models.
- 🌐 Integrated web research via Google Search API.
- 🤔 Reflective reasoning to identify knowledge gaps and refine searches.
- 📄 Generates answers with citations from gathered sources.
- 🔄 Hot-reloading for both frontend and backend during development.

## Project Structure

The project is divided into two main directories:

-   `frontend/`: Contains the React application built with Vite.
-   `backend/`: Contains the LangGraph/FastAPI application, including the research agent logic.

## Getting Started: Development and Local Testing

Follow these steps to get the application running locally for development and testing.

**1. Prerequisites:**

-   Node.js and npm (or yarn/pnpm)
-   Python 3.11+
-   **`GEMINI_API_KEY`**: The backend agent requires a Google Gemini API key.
    1.  Create a file named `.env` in the project root by copying the `.env.example` file.
    2.  Open the `.env` file and add your Gemini API key: `GEMINI_API_KEY="YOUR_ACTUAL_API_KEY"`

**2. Install Dependencies:**

**Backend:**

```bash
cd backend
pip install .
```

**Frontend:**

```bash
cd frontend
npm install
```

**3. Run Development Servers:**

**Backend & Frontend:**

```bash
make dev
```
This will run the backend and frontend development servers.    Open your browser and navigate to the frontend development server URL (e.g., `http://localhost:5173/app`).

_Alternatively, you can run the backend and frontend development servers separately. For the backend, open a terminal in the `backend/` directory and run `langgraph dev`. The backend API will be available at `http://127.0.0.1:2024`. It will also open a browser window to the LangGraph UI. For the frontend, open a terminal in the `frontend/` directory and run `npm run dev`. The frontend will be available at `http://localhost:5173`._

## How the Backend Agent Works (High-Level)

The core of the backend is a LangGraph agent defined in `backend/src/agent/graph.py`. It now follows a sophisticated four-stage workflow designed for automated research:

```mermaid
graph TD
    A[Start] --> B{1. Generate Initial Queries};
    B --> C{2. Execute Searches (Arxiv, etc.)};
    C --> D{3. Reflection & Refinement};
    D -- Insufficient --> C;
    D -- Sufficient --> E{4. Automated Resource Management};
    E --> F{5. RAG-based Knowledge Synthesis};
    F --> G{6. Automated Report Generation};
    G --> H[End];
```

1.  **Intelligent Literature Discovery & Reflection:**
    -   The agent takes a research topic and generates a set of initial search queries.
    -   It executes these queries against academic search APIs (like Arxiv).
    -   Crucially, it then enters a **reflection loop**. The agent analyzes the search results to see if they are sufficient.
    -   If there are knowledge gaps, it generates new queries and re-runs the search. This loop continues until the information is comprehensive or a maximum number of iterations is reached.

2.  **Automated Resource Management:**
    -   Once the literature search is complete, the agent finds DOIs (Digital Object Identifiers) in the collected abstracts.
    -   It uses the Unpaywall API to find open-access PDF versions of the papers.
    -   It then uses the Zotero API to automatically create a library entry for each paper, attaching the PDF if found.

3.  **RAG-based Knowledge Synthesis:**
    -   The agent downloads the full text from the discovered PDF URLs.
    -   It extracts the text, splits it into manageable chunks, and generates vector embeddings for each chunk using a Gemini model.
    -   These chunks and their embeddings are stored in a PostgreSQL database with the `pgvector` extension, creating a powerful Retrieval-Augmented Generation (RAG) knowledge base.

4.  **Automated Report Generation:**
    -   Finally, the agent uses the synthesized knowledge in the RAG database to generate a comprehensive report that answers the initial research topic, complete with citations.

## Project Upgrade Plan: Towards an Automated Research Platform

This project is undergoing a significant upgrade to transform it from a demo into a powerful, VS Code-native automated research platform. The development is divided into three phases.

### Phase 1: Backend Foundation and Core Agent (Complete)

This foundational phase has been completed. We have built a robust, "headless" AI agent that is callable via an API and fully implements the four-stage research workflow described above.

**Key deliverables from this phase:**
-   **Functional FastAPI Server:** The backend is served via FastAPI.
-   **PostgreSQL + pgvector DB:** A PostgreSQL database with the `pgvector` extension is integrated for RAG.
-   **Four-Stage LangGraph Agent:** The core agent logic is implemented in `backend/src/agent/graph.py`.
-   **Integrated Tooling:** The agent uses `arxiv`, `unpaywall`, `pyzotero`, and `litellm` to perform its tasks.
-   **Containerized Environment:** The entire backend stack can be run using Docker Compose.

### Phase 2: VS Code Skeleton and Static Display (In Progress)

The next phase focuses on building the user-facing component of the platform: a VS Code extension. The goal is to create a "read-only" view of the research process.

**Detailed Plan:**
1.  **Develop the basic VS Code Extension:**
    -   Set up a new TypeScript project for the extension.
    -   Implement the three-panel layout as described in the technical documentation:
        -   **Left Panel (Research Asset Library):** A TreeView to display research resources (papers, notes).
        -   **Center Panel (Dynamic Manuscript):** The main editor, where the final report will be shown.
        -   **Right Panel (AI Control Panel):** A Webview to show the agent's status and thinking process.
2.  **API Integration (Read-Only):**
    -   The extension will call the backend API to fetch the status and results of a completed research task.
    -   The data will be used to populate the three panels (e.g., list of papers in the asset library, final report in the editor, agent logs in the control panel).
3.  **Static Visualization:**
    -   The primary goal is to prove that the frontend can successfully connect to and display data from the backend. All interactions that trigger new runs will be handled via API tools (like Insomnia or curl) for now.

### Phase 3: Real-time Interaction and Dynamic Collaboration (Future)

The final phase will bring the platform to life by enabling full, real-time, two-way communication between the user and the agent.

**Detailed Plan:**
1.  **WebSocket Integration:**
    -   Implement WebSocket communication between the VS Code extension and the FastAPI backend.
    -   This will allow the agent to stream its "thoughts" and progress to the AI Control Panel in real-time.
2.  **Interactive Controls:**
    -   Build the UI components in the AI Control Panel (using React and the VS Code Webview UI Toolkit) that allow the user to:
        -   Start new research tasks with a natural language prompt.
        -   Observe the agent's progress.
        -   Implement "human-in-the-loop" (HITL) decision points, where the agent pauses and asks for user input before proceeding.
3.  **Dynamic Document Editing:**
    -   The agent will be able to directly edit the Markdown file in the center panel using the VS Code Workspace API. This will allow the agent to collaboratively write the report with the user.


## Technologies Used

- [React](https://reactjs.org/) (with [Vite](https://vitejs.dev/)) - For the frontend user interface.
- [Tailwind CSS](https://tailwindcss.com/) - For styling.
- [Shadcn UI](https://ui.shadcn.com/) - For components.
- [LangGraph](https://github.com/langchain-ai/langgraph) - For building the backend research agent.
- [Google Gemini](https://ai.google.dev/models/gemini) - LLM for query generation, reflection, and answer synthesis.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Tools

This project includes a collection of utility scripts located in the `scripts` directory. These tools are managed and executed via the root `Makefile`.

### List Models

This tool fetches the list of available models from the Google Generative AI API and saves them to `logs/models.log`.

**Prerequisites:**

-   Ensure the `GEMINI_API_KEY` environment variable is set.

**Usage:**

Run the following command from the project root directory:
    ```bash
    make list-models
    ``` 
