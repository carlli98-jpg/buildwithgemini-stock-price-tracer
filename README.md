# Stock Price Tracer

Stock Price Tracer is a financial AI assistant built using the Google Agent Development Kit (ADK) and Agent Engine. It helps users manage a stock portfolio, get live market data, convert currencies, and generate financial graphics—all presented in a rich, card-based chat interface.

## Features & Capabilities

- **Live Market Data:** Fetches real-time stock prices, percentage changes, and market statistics using the Yahoo Finance API (`fetch_live_stock_quote`).
- **Currency Conversions:** Converts stock and portfolio valuations into multiple international currencies using the free ExchangeRate API (`get_currency_exchange_rates`).
- **Portfolio Tracking (Firestore):** Allows users to add, update, and remove tracked stocks from a persisted watchlist stored in a **Firestore** database backend (`get_tracked_stocks`, `add_or_update_stock`, etc.).
- **Image & Badge Generation:** Creates stock brand badges and financial charts using the `gemini-3.1-flash-lite-image` model. Generated images are saved as session artifacts and uploaded directly to a public **Google Cloud Storage** bucket, returning a live HTTPS URL (`generate_stock_image`).
- **Advanced Code Execution:** Uses `AgentEngineSandboxCodeExecutor` to securely run Python code in a Vertex AI **Sandbox** for complex financial modeling, compound interest projections, and data analysis.
- **Cross-Session Memory:** Retains user preferences, goals, and facts (such as allergies/dietary restrictions) across sessions using the **Vertex AI Memory Bank** (`PreloadMemoryTool` and callback).
- **Rich UI Cards (A2UI):** The agent generates structured visual components (A2UI v0.8) displaying portfolios and stock details directly inside the chat, seamlessly configured using the `A2uiSchemaManager`.
- **Custom Chat Frontend:** Includes a custom FastAPI proxy and HTML chat frontend (`/frontend`) running over the A2A protocol. It securely connects to the deployed Agent Runtime endpoint and natively renders the agent's A2UI cards.

## Setup and Running Locally

To run the custom chat frontend locally connecting to your deployed agent:

1. **Install dependencies:**
   Make sure you have `uv` installed, then set up the frontend dependencies:
   ```bash
   cd frontend
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

2. **Configure the environment:**
   Ensure you have a `.env` file in the `frontend/` directory with your Agent Engine resource name:
   ```env
   AGENT_ENGINE_RESOURCE_NAME="projects/<project_number>/locations/<region>/reasoningEngines/<id>"
   AGENT_DIRECTORY="app"
   ```

3. **Start the local chat frontend:**
   ```bash
   python main.py
   ```
   The local web server will launch (typically on port 8080 or 8081). Open the printed address in your browser to interact with the agent.

4. **Or test the agent via the terminal over A2A:**
   ```bash
   agents-cli run --mode a2a "list my tracked stocks"
   ```

## Cloud Deployment

- **Agent Backend (Agent Engine):** The core agent is deployed as an A2A Reasoning Engine on Google Cloud using `agents-cli deploy`.
- **Frontend (Cloud Run):** The FastAPI proxy and chat UI are containerized and deployed to Cloud Run, securely invoking the backend agent using Application Default Credentials (`roles/aiplatform.user`).
