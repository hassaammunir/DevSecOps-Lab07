from fastapi.testclient import TestClient
from app import app

client = TestClient(app, raise_server_exceptions=False)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_existing_student():
    response = client.get("/search", params={"name": "Alice"})
    assert response.json() == {"students": ["Alice"]}


def test_missing_student():
    response = client.get("/search", params={"name": "Unknown"})
    assert response.json() == {"students": []}


def test_name_with_apostrophe():
    response = client.get("/search", params={"name": "O'Neil"})
    assert response.status_code == 200
    assert response.json() == {"students": ["O'Neil"]}


# ---- Task 3: three additional cases ----
def test_empty_input():
    """Empty input is handled safely and matches no student."""
    response = client.get("/search", params={"name": ""})
    assert response.status_code == 200
    assert response.json() == {"students": []}


def test_numeric_input():
    """A numeric string is treated as data, not SQL, and matches nothing."""
    response = client.get("/search", params={"name": "12345"})
    assert response.status_code == 200
    assert response.json() == {"students": []}


def test_special_characters_injection():
    """A classic SQL-injection payload is treated as literal data (no bypass)."""
    response = client.get("/search", params={"name": "' OR '1'='1"})
    assert response.status_code == 200
    assert response.json() == {"students": []}
