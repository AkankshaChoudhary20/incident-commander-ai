from datetime import datetime, timezone

from app.analyzer import analyze
from app.models import Signal


def test_detects_memory_exhaustion():
    signals = [
        Signal(
            incident_id="INC-1",
            source="kubernetes",
            type="log",
            message="Container terminated: OOM out of memory",
            timestamp=datetime.now(timezone.utc),
            severity="critical",
            service="payments",
        )
    ]
    causes, remediations = analyze(signals)
    assert causes[0].cause == "Memory exhaustion"
    assert causes[0].confidence >= 0.7
    assert remediations
