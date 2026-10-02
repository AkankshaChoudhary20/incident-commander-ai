from app.analyzer import analyze
from app.models import IncidentReport, Signal
from app.store import add_signal, get_signals

SEVERITY_ORDER = {"info": 1, "warning": 2, "critical": 3}


def ingest(signal: Signal) -> int:
    return add_signal(signal)


def build_report(incident_id: str) -> IncidentReport | None:
    signals = get_signals(incident_id)
    if not signals:
        return None

    causes, remediations = analyze(signals)
    severity = max(signals, key=lambda item: SEVERITY_ORDER[item.severity]).severity
    return IncidentReport(
        incident_id=incident_id,
        severity=severity,
        services=sorted({signal.service for signal in signals}),
        timeline=signals,
        root_causes=causes,
        remediations=remediations,
    )
