from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_chat_endpoint():
    response = client.post(
        "/api/v1/chat",
        json={
            "session_id": "test-001",
            "message": "What should I focus on selling?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["session_id"] == "test-001"
    assert data["response"]
    assert data["message_count"] > 0


def test_memory_same_session():
    session_id = "memory-test-001"

    first = client.post(
        "/api/v1/chat",
        json={
            "session_id": session_id,
            "message": "My business sells clothes."
        }
    )

    assert first.status_code == 200

    second = client.post(
        "/api/v1/chat",
        json={
            "session_id": session_id,
            "message": "What does my business sell?"
        }
    )

    assert second.status_code == 200

    data = second.json()

    assert data["session_id"] == session_id
    assert data["message_count"] >= 2


def test_knowledge_cutoff_instruction():
    response = client.post(
        "/api/v1/chat",
        json={
            "session_id": "cutoff-test-001",
            "message": "What happened in 2025?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response"]


def test_no_web_search_instruction():
    response = client.post(
        "/api/v1/chat",
        json={
            "session_id": "web-test-001",
            "message": "Search the web and tell me today's latest business news."
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response"]
