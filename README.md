# Tutor Module

An AI-powered tutoring system that provides personalized, step-by-step academic explanations using a locally-hosted large language model. Built with FastAPI, Ollama, and Streamlit, it answers student questions across subjects, recommends learning resources, and generates practice questions — all without sending data to external APIs.

---

## Demo

![Tutor UI](screenshots/ui.PNG)
![Tutor Response](screenshots/response.PNG)

---

## Features

- **Conversational tutoring** with step-by-step explanations adapted to subject and difficulty
- **Auto-detection** of subject (Math, English, Biology) and concept from the student's question, so users don't need to manually classify
- **Curated resource recommendations** — links to videos, articles, and practice material per concept
- **Visual aids** — diagrams and interactive resources surfaced based on the topic
- **Practice question generation** — the tutor can generate follow-up questions on the same concept
- **Interaction history** — Q&A logs persisted per student for review and analytics
- **Local-first** — runs entirely on your machine via Ollama; no external API keys, no per-token costs

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | FastAPI + Uvicorn | Async-ready, automatic OpenAPI docs, fast iteration |
| Model runtime | Ollama | Local LLM inference, no API costs, full data privacy |
| Model | Gemma 2B | Small enough to run on consumer hardware, quality sufficient for tutoring |
| Frontend | Streamlit | Rapid UI iteration, native support for markdown and LaTeX rendering |
| Persistence | JSON (current) | Simple and portable; SQLite migration planned |

---

## Architecture

```
┌─────────────────────┐
│  Streamlit UI       │  ← User asks question
│  (tutor_ui.py)      │
└──────────┬──────────┘
           │ POST /tutor/query
           ▼
┌─────────────────────┐
│  FastAPI Backend    │  ← Routes, validation, orchestration
│  (routes.py)        │
└──────────┬──────────┘
           │
           ├──► Subject & concept detection
           ├──► Prompt builder (prompt_engine.py)
           ├──► Resource lookup (recommender.py)
           ├──► History logging (history.py)
           │
           ▼
┌─────────────────────┐
│  Gemma Engine       │  ← HTTP call to Ollama
│  (gemma_engine.py)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Ollama (localhost) │  ← Local LLM inference
│  gemma:2b           │
└─────────────────────┘
```

---

## Project Structure

```
Tutor Module/
├── app/
│   ├── main.py             # FastAPI app entry point + model warmup
│   ├── routes.py           # API route definitions
│   ├── models.py           # Pydantic request/response schemas
│   ├── gemma_engine.py     # Ollama HTTP client
│   ├── prompt_engine.py    # Prompt construction for queries and practice
│   ├── recommender.py      # Resource and visual aid lookup
│   ├── history.py          # Interaction logging and retrieval
│   ├── user_manager.py     # Student profile management
│   ├── tutor_ui.py         # Streamlit frontend
│   └── test_api.py         # API smoke tests
├── screenshots/            # README images
├── static/                 # Static assets
├── qa_history.json         # Interaction log (gitignored)
├── user_profiles.json      # User profiles (gitignored)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running
- ~4 GB free RAM (gemma:2b uses ~1.7 GB plus overhead)

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd "Tutor Module"

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Pull the Gemma model
ollama pull gemma:2b
```

### Running

You'll need three terminals (or one terminal with a process manager).

**Terminal 1 — Ollama** (typically auto-starts as a background service after install):
```bash
ollama serve
```

**Terminal 2 — Backend:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8500 --reload
```

The backend warms the model on startup, so the first request is fast. API docs are at `http://localhost:8500/docs`.

**Terminal 3 — Frontend:**
```bash
streamlit run app/tutor_ui.py
```

The UI opens automatically at `http://localhost:8501`.

---

## API Reference

### `POST /tutor/query`
Main tutoring endpoint. Returns a step-by-step explanation, resource links, and visual aids.

**Request:**
```json
{
  "student_id": "guest_001",
  "question": "How do I solve a quadratic equation?",
  "course": "Algebra I",
  "subject": "Math",
  "difficulty": "medium",
  "concept": "quadratic_equations"
}
```

`subject` and `concept` are auto-detected from the question if omitted.

**Response:**
```json
{
  "response": "Step-by-step explanation...",
  "resources": ["https://..."],
  "visuals": ["https://..."],
  "subject": "math",
  "concept": "quadratic_equations"
}
```

### `POST /tutor/practice`
Generates a practice question on the same concept after a tutor explanation.

### `POST /tutor/recommend`
Returns recommended resources for a topic the student is struggling with.

### `GET /history`
Retrieves a student's Q&A history, optionally filtered by course or date.

---

## Known Limitations & Future Work

This is an early-stage project. Areas I'd improve next, in priority order:

- **Persistence layer** — Migrate from JSON files to SQLite for atomic writes, indexed queries, and concurrent access. The `/history` endpoint scales poorly with the current approach.
- **Streaming responses** — Ollama supports `stream: true`, and Streamlit's `st.write_stream` can render tokens as they arrive. Total time stays the same, but the perceived UX improves significantly.
- **Schema flexibility** — The Pydantic `QueryRequest` is strict; making more fields optional with defaults would reduce 422 errors when the UI and API drift.
- **Async backend** — Ollama calls currently block via `requests`. Switching to `httpx.AsyncClient` would let FastAPI handle concurrent requests properly.
- **Test coverage** — The keyword-based subject and concept detectors in `routes.py` are fragile. Unit tests would catch regressions when the keyword maps are extended.
- **Error UX** — When the model times out, the user sees a generic error. Better messaging and retry logic would help.
- **Larger model option** — gemma:2b is fast but limited. Adding a config flag to switch to a larger model (e.g., gemma:7b or llama3) on capable hardware would broaden the project's usefulness.

---

## License

MIT