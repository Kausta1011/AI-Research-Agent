# AI Research Agent

An autonomous AI agent that takes your research question, searches 
the web, evaluates its findings, and delivers a structured research 
report — all without any manual input.

## Live Demo
Try it here → https://ai-research-agent-yo5sdpneigrh7qmzqzmwta.streamlit.app

Backend API docs → https://ai-research-agent-2026.onrender.com/docs

---

## Architecture
```
User Question
      ↓
Streamlit UI (app.py)
      ↓ HTTP POST
FastAPI Backend (api.py)
      ↓
LangGraph Agent (agent.py)
      ↓
  ┌─────────────────────────────┐
  │         Agent Loop          │
  │                             │
  │  THINKING                   │
  │  Groq generates search query│
  │         ↓                   │
  │  ACTING                     │
  │  Tavily searches the web    │
  │         ↓                   │
  │  SHOULD CONTINUE?           │
  │  Groq evaluates results     │
  │         ↓            ↓      │
  │  enough?          missing?  │
  │         ↓            ↓      │
  │  FINAL ANSWER     THINKING  │
  │  Groq writes      loop back │
  │  report                     │
  └─────────────────────────────┘
      ↓
Structured Research Report
with Sources and URLs
```

---

## How It Works

1. **Thinking** — the agent receives your question and uses Groq 
   (Llama 3.3 70B) to generate a concise, optimized search query

2. **Acting** — it searches the real web using Tavily API and 
   retrieves up-to-date sources from authoritative websites

3. **Evaluating** — Groq evaluates whether the retrieved information 
   is sufficient to answer the original question comprehensively

4. **Looping** — if results are insufficient, the agent identifies 
   exactly what is missing and autonomously searches again with a 
   refined query — no human input required

5. **Reporting** — once satisfied, it synthesizes all sources into 
   a clean, structured research report complete with references and URLs

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Agent framework | LangGraph | Manages the ReAct agent loop |
| LLM | Groq — Llama 3.3 70B | Reasoning, search queries, report writing |
| Web search | Tavily API | Real-time web search |
| Backend | FastAPI | REST API endpoint |
| Frontend | Streamlit | User interface |
| Deployment | Render | Backend hosting |
| Deployment | Streamlit Cloud | Frontend hosting |

---

## Project Structure
```
AI-Research-Agent/
├── state.py          # AgentState — shared memory across nodes
├── agent.py          # LangGraph graph — nodes, edges, ReAct loop
├── api.py            # FastAPI — REST endpoint
├── app.py            # Streamlit — frontend UI
├── requirements.txt  # dependencies
└── .gitignore
```

---

## What I Learned

This was my first agentic AI project. Coming in with experience in 
FastAPI, Groq and Streamlit but zero LangGraph knowledge, the biggest 
challenge was understanding the agentic paradigm from scratch:

- What separates an **agent** from a **pipeline**
- How **LangGraph state** flows between nodes
- How the **ReAct loop** (Reason → Act → Observe) works in practice
- How a **conditional edge** makes the LLM the decision maker
- How to wire **Groq and Tavily** as tools inside a graph

Built in one week from zero to a fully deployed, portfolio-ready project.

---

## Run Locally
```bash
git clone https://github.com/Kausta1011/AI-Research-Agent
cd AI-Research-Agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```
```bash
# Terminal 1 — start backend
uvicorn api:app --reload

# Terminal 2 — start frontend
streamlit run app.py
```

Open → http://localhost:8501

---

## Author
Kaustubh Salunke
GitHub → https://github.com/Kausta1011
