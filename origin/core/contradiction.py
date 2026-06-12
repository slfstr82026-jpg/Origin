"""Interference and scientific contradiction calculations."""

from __future__ import annotations

from dataclasses import dataclass

from origin.core.phase_math import WaveComponent, interference_score


@dataclass(frozen=True)
class ContradictionResult:
    """Contradiction index result for competing cause and treatment evidence."""

    ci: float
    relation: str
    protocol: str | None = None
    message: str | None = None


def scientific_contradiction_index(e_treat: float, e_cause: float) -> float:
    """Calculate CI = |E_treat - E_cause| / (E_treat + E_cause)."""
    denominator = abs(e_treat) + abs(e_cause)
    if denominator == 0:
        return 0.0
    return abs(e_treat - e_cause) / denominator


def scientific_contradiction_protocol(ci: float, destructive: bool = False, threshold: float = 0.1) -> str | None:
    """Activate SCIENTIFIC_CONTRADICTION for destructive near-balanced evidence."""
    if destructive or ci <= threshold:
        return "SCIENTIFIC_CONTRADICTION"
    return None


def contradiction_index(left: WaveComponent, right: WaveComponent) -> ContradictionResult:
    """Calculate contradiction from wave interference compatibility."""
    compatibility = interference_score(left, right)
    destructive = compatibility < 0
    ci = scientific_contradiction_index(left.amplitude, right.amplitude)
    protocol = scientific_contradiction_protocol(ci, destructive=destructive)
    if protocol:
        relation = "research_gap"
        message = "Destructive or balanced interference indicates a scientific contradiction requiring human review."
    elif compatibility >= 0.5:
        relation = "supportive"
        message = "Wave evidence is constructively aligned."
    else:
        relation = "ambiguous"
        message = "Wave evidence is weakly aligned and needs more evidence."
    return ContradictionResult(ci=ci, relation=relation, protocol=protocol, message=message)
