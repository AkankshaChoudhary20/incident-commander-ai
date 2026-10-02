from fastapi.testclient import TestClient

from app.main import app
from app.store import clear

client = TestClient(app)


def setup_function():
    clear()


def test_incident_workflow():
    payload = {
        "incident_id": "INC-42",
        "source": "kubernetes",
        "type": "alert",
        "message": "payment-api is in CrashLoopBackOff",
        "timestamp": "2026-10-02T04:00:00Z",
        "severity": "critical",
        "service": "payment-api",
    }
    response = client.post("/api/v1/signals", json=payload)
    assert response.status_code == 201

    response = client.get("/api/v1/incidents/INC-42")
    assert response.status_code == 200
    data = response.json()
    assert data["severity"] == "critical"
    assert data["root_causes"][0]["cause"] == "Repeated workload startup failure"


def test_unknown_incident_returns_404():
    assert client.get("/api/v1/incidents/missing").status_code == 404
