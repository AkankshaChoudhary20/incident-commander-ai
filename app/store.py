from collections import defaultdict

from app.models import Signal

_signals: dict[str, list[Signal]] = defaultdict(list)


def add_signal(signal: Signal) -> int:
    _signals[signal.incident_id].append(signal)
    return len(_signals[signal.incident_id])


def get_signals(incident_id: str) -> list[Signal]:
    return sorted(_signals.get(incident_id, []), key=lambda item: item.timestamp)


def clear() -> None:
    _signals.clear()
