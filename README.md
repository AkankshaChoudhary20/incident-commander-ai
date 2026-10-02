# Incident Commander AI

AI-assisted SRE incident investigation platform that turns alerts and logs into a structured incident timeline, likely root causes, and actionable remediation guidance.

## Features

- Ingest alerts and application/infrastructure logs
- Normalize and correlate incident signals
- Build an incident timeline automatically
- Rank likely root causes using deterministic evidence scoring
- Generate remediation recommendations
- Optional Amazon Bedrock explanation layer
- FastAPI REST API with interactive Swagger docs
- Docker support and GitHub Actions CI
- Safe-by-design: recommends actions but does not mutate infrastructure

## Architecture

```text
Alerts / Logs
     |
     v
FastAPI Ingestion API
     |
     v
Signal Normalizer
     |
     +----> Timeline Builder
     |
     +----> Root Cause Analyzer
                    |
                    v
          Remediation Engine
                    |
                    v
       Optional Amazon Bedrock
                    |
                    v
          Incident Report API
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs`.

## Example workflow

1. POST alerts/logs to `/api/v1/signals`.
2. GET `/api/v1/incidents/{incident_id}` for the correlated incident report.
3. POST `/api/v1/incidents/{incident_id}/explain` for a human-readable explanation.

## Tech stack

Python, FastAPI, Pydantic, Amazon Bedrock (optional), Docker, Pytest, GitHub Actions.

## Disclaimer

This project is an incident-analysis assistant. Validate recommendations before applying changes to production systems.
