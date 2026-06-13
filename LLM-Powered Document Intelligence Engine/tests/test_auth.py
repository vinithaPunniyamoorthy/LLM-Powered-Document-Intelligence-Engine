import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_and_login():
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"
    register = client.post(
        "/auth/register",
        json={"name": "Test User", "email": email, "password": "secret123"},
    )
    assert register.status_code == 200

    login = client.post(
        "/auth/login",
        json={"email": email, "password": "secret123"},
    )
    assert login.status_code == 200
    payload = login.json()
    assert "access_token" in payload
    assert payload["token_type"] == "bearer"
