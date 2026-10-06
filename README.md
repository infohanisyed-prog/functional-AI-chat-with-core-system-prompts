# HisabDo AI - FastAPI Chat API

Initial prototype for the HisabDo AI Business Assistant.

## Features

- FastAPI backend
- `POST /api/v1/chat`
- HisabDo AI system prompt
- Basic session-based conversation memory
- Request/response logging
- Health endpoint
- Pytest API tests
- Groq LLM integration

## 1. Create environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

## 2. Install dependencies

```powershell
pip install -r requirements.txt
```

## 3. Configure Groq

Copy `.env.example` to `.env` and put your Groq API key in it.

Then, before starting the app, load the environment variables in your shell or add `python-dotenv` loading to your startup. For a simple local setup, PowerShell can use:

```powershell
$env:GROQ_API_KEY="your_key_here"
$env:GROQ_MODEL="llama-3.1-8b-instant"
```

## 4. Start API

From the project root:

```powershell
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

## 5. Test chat in Swagger

Open `/docs`, select `POST /api/v1/chat`, click **Try it out**, and send:

```json
{
  "session_id": "demo-001",
  "message": "How can I improve my business cash flow?"
}
```

## 6. Run automated tests

```powershell
pytest
```

The tests use a fake LLM, so they do not consume Groq API credits.
