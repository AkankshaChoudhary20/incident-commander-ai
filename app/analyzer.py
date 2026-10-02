from app.models import Remediation, RootCause, Signal

RULES = [
    (
        ("connection refused", "connection reset", "timeout"),
        "Downstream dependency or network connectivity failure",
        "Check dependency health, DNS, network policy, security groups, and recent deployments.",
    ),
    (
        ("out of memory", "oom", "memory limit"),
        "Memory exhaustion",
        "Inspect memory usage and limits; identify leaks or abnormal workload before scaling.",
    ),
    (
        ("disk full", "no space left"),
        "Disk capacity exhaustion",
        "Inspect filesystem usage, logs, and retention policies; reclaim capacity safely.",
    ),
    (
        ("5xx", "500", "503", "internal server error"),
        "Application or upstream service failure",
        "Inspect application errors, dependency health, and recent changes.",
    ),
    (
        ("crashloopbackoff", "crash loop"),
        "Repeated workload startup failure",
        "Inspect container logs, probes, configuration, secrets, and the latest deployment.",
    ),
]


def analyze(signals: list[Signal]) -> tuple[list[RootCause], list[Remediation]]:
    text = " ".join(s.message.lower() for s in signals)
    causes: list[RootCause] = []
    remediations: list[Remediation] = []

    for keywords, cause, action in RULES:
        matches = [keyword for keyword in keywords if keyword in text]
        if not matches:
            continue
        confidence = min(0.95, 0.55 + 0.1 * len(matches))
        evidence = [
            s.message for s in signals
            if any(keyword in s.message.lower() for keyword in keywords)
        ][:3]
        causes.append(RootCause(cause=cause, confidence=confidence, evidence=evidence))
        remediations.append(
            Remediation(
                priority="high" if confidence >= 0.75 else "medium",
                action=action,
                rationale=f"Matched incident evidence: {', '.join(matches)}.",
            )
        )

    if not causes:
        causes.append(
            RootCause(
                cause="Insufficient evidence for a specific root cause",
                confidence=0.25,
                evidence=[s.message for s in signals[:3]],
            )
        )
        remediations.append(
            Remediation(
                priority="low",
                action="Collect additional application, infrastructure, and dependency telemetry.",
                rationale="Current signals do not strongly match a known failure pattern.",
            )
        )

    causes.sort(key=lambda item: item.confidence, reverse=True)
    return causes, remediations
