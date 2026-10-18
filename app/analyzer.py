import re

from app.models import Remediation, RootCause, Signal

RULES = [
    (
        ("connection refused", "connection reset", "timeout"),
        "Downstream dependency or network connectivity failure",
        "Check dependency health, DNS, network policy, security groups, and recent deployments.",
    ),
    (
        ("out of memory", "oom", "oomkilled", "memory limit"),
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


def matches_keyword(message: str, keyword: str) -> bool:
    if keyword in {"oom", "500", "503", "5xx"}:
        return re.search(r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])", message) is not None
    suffix = r"s?" if keyword == "timeout" else ""
    return re.search(r"(?<![a-z0-9])" + re.escape(keyword) + suffix + r"(?![a-z0-9])", message) is not None


def analyze(signals: list[Signal]) -> tuple[list[RootCause], list[Remediation]]:
    causes: list[RootCause] = []
    remediations: list[Remediation] = []

    for keywords, cause, action in RULES:
        matches = [keyword for keyword in keywords if any(matches_keyword(signal.message.lower(), keyword) for signal in signals)]
        if not matches:
            continue
        confidence = min(0.95, 0.55 + 0.1 * len(matches))
        evidence = [
            s.message for s in signals
            if any(matches_keyword(s.message.lower(), keyword) for keyword in keywords)
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

    ranked = sorted(zip(causes, remediations), key=lambda pair: pair[0].confidence, reverse=True)
    return [cause for cause, _ in ranked], [remediation for _, remediation in ranked]

