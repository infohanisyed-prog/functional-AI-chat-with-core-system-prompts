from fastapi.testclient import TestClient

from app.main import app, memory

client = TestClient(app)


class FakeLLM:
    def generate(self, history):
        return "This is a test response from HisabDo AI."


def setup_function():
    memory._sessions.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat():
    import app.main as main

    main.llm = FakeLLM()

    response = client.post(
        "/api/v1/chat",
        json={
            "session_id": "test-session",
            "message": "How can I track business expenses?",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "test-session"
    assert "test response" in data["response"]
    assert data["message_count"] == 2


def test_chat_keeps_conversation_context():
    import app.main as main

    class ContextFakeLLM:
        def generate(self, history):
            assert history[0]["content"] == "My business is a clothing store."
            assert history[1]["content"] == "What should I focus on?"
            return "Use the previous business context."

    main.llm = ContextFakeLLM()

    client.post(
        "/api/v1/chat",
        json={
            "session_id": "context-session",
            "message": "My business is a clothing store.",
        },
    )
    response = client.post(
        "/api/v1/chat",
        json={
            "session_id": "context-session",
            "message": "What should I focus on?",
        },
    )

    assert response.status_code == 200
    assert response.json()["message_count"] == 4


def test_empty_message_is_rejected():
    response = client.post(
        "/api/v1/chat",
        json={"session_id": "test", "message": ""},
    )
    assert response.status_code == 422
