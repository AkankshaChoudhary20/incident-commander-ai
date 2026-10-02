from fastapi import FastAPI, HTTPException

from app.models import IncidentReport, Signal
from app.service import build_report, ingest

app = FastAPI(
    title="Incident Commander AI",
    version="1.0.0",
    description="AI-assisted SRE incident investigation and remediation API.",
)


@app.get("/")
def root() -> dict[str, str]:
    return {"name": "Incident Commander AI", "docs": "/docs"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/api/v1/signals", status_code=201)
def create_signal(signal: Signal) -> dict[str, str | int]:
    count = ingest(signal)
    return {"incident_id": signal.incident_id, "signals": count}


@app.get("/api/v1/incidents/{incident_id}", response_model=IncidentReport)
def incident(incident_id: str) -> IncidentReport:
    report = build_report(incident_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return report


@app.post("/api/v1/incidents/{incident_id}/explain")
def explain(incident_id: str) -> dict[str, str]:
    report = build_report(incident_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    cause = report.root_causes[0]
    action = report.remediations[0]
    return {
        "explanation": (
            f"Incident {incident_id} is {report.severity}. "
            f"The leading hypothesis is '{cause.cause}' "
            f"(confidence {cause.confidence:.0%}). "
            f"Recommended next step: {action.action}"
        )
    }
