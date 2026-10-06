import logging
import time

from fastapi import FastAPI, HTTPException

from .llm import GroqChatService
from .memory import ConversationMemory
from .models import ChatRequest, ChatResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("hisabdo-ai")

app = FastAPI(
    title="HisabDo AI Chat API",
    version="0.1.0",
    description="Initial AI Business Assistant API prototype.",
)

memory = ConversationMemory(max_messages=20)
llm = None


def get_llm() -> GroqChatService:
    global llm
    if llm is None:
        llm = GroqChatService()
    return llm


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "hisabdo-ai",
        "version": app.version,
    }


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    started = time.perf_counter()

    logger.info(
        "chat_request session_id=%s message_length=%d",
        request.session_id,
        len(request.message),
    )

    memory.add(request.session_id, "user", request.message)
    history = memory.get(request.session_id)

    try:
        response = get_llm().generate(history)
        if not response.strip():
            raise RuntimeError("The AI model returned an empty response.")

        memory.add(request.session_id, "assistant", response)

        elapsed = time.perf_counter() - started
        logger.info(
            "chat_response session_id=%s status=200 duration=%.3fs",
            request.session_id,
            elapsed,
        )

        return ChatResponse(
            session_id=request.session_id,
            response=response,
            message_count=memory.count(request.session_id),
        )

    except Exception as exc:
        logger.exception(
            "chat_error session_id=%s duration=%.3fs",
            request.session_id,
            time.perf_counter() - started,
        )
        # Remove the unsatisfied user turn so a failed request does not
        # pollute the conversation history.
        history_after_failure = memory.get(request.session_id)
        if history_after_failure and history_after_failure[-1] == {
            "role": "user",
            "content": request.message,
        }:
            memory._sessions[request.session_id] = history_after_failure[:-1]

        raise HTTPException(
            status_code=502,
            detail="AI service is temporarily unavailable.",
        ) from exc
