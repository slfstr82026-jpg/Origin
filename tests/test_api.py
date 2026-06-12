import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from origin.api.server import create_app


def test_reason_endpoint_returns_grounded_placeholder():
    client = TestClient(create_app())

    response = client.post("/reason", json={"question": "What causes glucose?"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["confidence"] == 1.0
    assert payload["path"] == ["glucose"]
