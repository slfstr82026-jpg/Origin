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


def test_core_api_layers():
    client = TestClient(create_app())
    edges = [{"source": "a", "target": "b", "weight": 0.8, "label": "causes", "evidence": 0.9}]

    graph_response = client.post("/graph/query", json={"focus": "a", "edges": edges})
    wave_response = client.post("/wave/simulate", json={"start": "a", "edges": edges})
    contradiction_response = client.post("/contradiction", json={"e_treat": 0.8, "e_cause": 0.8})
    explain_response = client.post("/explain", json={"focus": "a", "edges": edges})

    assert graph_response.status_code == 200
    assert wave_response.status_code == 200
    assert contradiction_response.json()["protocol"] == "SCIENTIFIC_CONTRADICTION"
    assert explain_response.json()["path"] == ["a", "b"]
