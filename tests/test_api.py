from fastapi.testclient import TestClient

from app import rag
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ask_endpoint_with_fake_llm(monkeypatch):
    fake_results = [
        {
            "text": "Feed dry and green fodder daily.",
            "metadata": {
                "source": "NDDB Handbook",
                "page": 5,
            },
        }
    ]

    monkeypatch.setattr(
        rag,
        "search_similar",
        lambda query, top_k: fake_results,
    )

    monkeypatch.setattr(
        rag,
        "generate_response",
        lambda prompt: "Feed dry and green fodder daily.",
    )

    response = client.post(
        "/ask",
        json={"question": "How should I feed dairy animals?"},
    )

    assert response.status_code == 200
    assert "answer" in response.json()
    assert "citations" in response.json()


def test_ask_endpoint_rejects_empty_question():
    response = client.post(
        "/ask",
        json={"question": "   "},
    )

    assert response.status_code == 400