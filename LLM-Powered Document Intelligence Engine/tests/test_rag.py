from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_query_without_documents_returns_guidance():
    response = client.post("/query", json={"question": "What is this project about?"})
    assert response.status_code == 200
    body = response.json()
    assert "answer" in body
    assert isinstance(body["answer"], str)
