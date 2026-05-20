# Nivara — AI Financial Advisor

Nivara is a full-stack AI-powered financial advisor chatbot built for Indian investors. It uses a **multi-agent architecture** (LangGraph) to route user queries to the right specialist agent: educational Q&A, live stock data, or personalised portfolio planning.

---

## Architecture

```
User (Next.js Frontend)
        │  JWT + SSE streaming
        ▼
FastAPI Backend (main.py)
        │
        ▼
Supervisor Agent (GPT-4o) — routes queries
    ├── RAGAgent       — Answers finance concepts via Milvus vector DB
    ├── MarketAgent    — Fetches live/historical data from Yahoo Finance
    └── PlannerAgent   — Generates Equity/Gold/Debt allocation via ML model
```

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | ≥ 3.10 |
| Node.js | ≥ 18 |
| PostgreSQL | ≥ 14 |

You will also need accounts / API keys for:
- **OpenAI** (GPT-4o)
- **NVIDIA AI Endpoints** (embedding model)
- **Zilliz Cloud** (Milvus vector database)

---

## Backend Setup

```bash
cd Backend

# 1. Create and activate a virtual environment
python -m venv nivara_venv
nivara_venv\Scripts\activate          # Windows
# source nivara_venv/bin/activate     # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
copy .env.example .env
# Edit .env and fill in all values

# 4. Start the server
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs: `http://127.0.0.1:8000/docs`

### API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/signup` | — | Register a new user |
| POST | `/login` | — | Login and receive a JWT |
| POST | `/chat-stream` | Bearer JWT | Stream a chat response (SSE) |
| GET | `/` | — | Health check |

---

## Frontend Setup

```bash
cd nivara-frontend

# 1. Install dependencies
npm install

# 2. Start the development server
npm run dev
```

The app will be available at `http://localhost:3000`.

> The frontend expects the backend to be running at `http://127.0.0.1:8000`.  
> To change this, update `API_URL` in `src/app/page.tsx`.

---

## Environment Variables

See [`Backend/.env.example`](Backend/.env.example) for the full list of required variables.

---

## Agents

| Agent | Trigger | Data Source |
|-------|---------|-------------|
| **RAGAgent** | "What is SIP?", "Explain PPF" | Milvus vector DB (financial documents) |
| **MarketAgent** | Stock tickers like `RELIANCE.NS`, `TSLA` | Yahoo Finance |
| **PlannerAgent** | "I want to invest", "Create a plan" | Trained scikit-learn model |

---

## Notes

- **CORS**: Currently set to `allow_origins=["*"]` for development. Restrict this in production.
- **Conversation memory**: Each user has a persistent `thread_id` stored in the database, so conversations continue across sessions.
- **Streaming**: Responses are streamed token-by-token using Server-Sent Events (SSE).
