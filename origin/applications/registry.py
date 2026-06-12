"""Application layer domain registry."""

from __future__ import annotations

APPLICATION_DOMAINS = {
    "medical_ai": "diagnosis and treatment reasoning",
    "policy_analysis": "policy intervention and outcome analysis",
    "cybersecurity": "attack-path and risk propagation analysis",
    "risk_analysis": "enterprise and systemic risk analysis",
    "scientific_research": "hypothesis and contradiction discovery",
}


def supported_domains() -> list[str]:
    """Return supported application domains."""
    return list(APPLICATION_DOMAINS)
