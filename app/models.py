from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class SignalType(str, Enum):
    alert = "alert"
    log = "log"


class Signal(BaseModel):
    incident_id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    type: SignalType
    message: str = Field(min_length=1)
    timestamp: datetime
    severity: Literal["info", "warning", "critical"] = "warning"
    service: str = "unknown"


class RootCause(BaseModel):
    cause: str
    confidence: float = Field(ge=0, le=1)
    evidence: list[str]


class Remediation(BaseModel):
    priority: Literal["high", "medium", "low"]
    action: str
    rationale: str


class IncidentReport(BaseModel):
    incident_id: str
    severity: str
    services: list[str]
    timeline: list[Signal]
    root_causes: list[RootCause]
    remediations: list[Remediation]
