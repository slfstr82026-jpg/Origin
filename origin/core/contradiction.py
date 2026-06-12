"""Contradiction index (CI) calculations."""

from __future__ import annotations

from dataclasses import dataclass

from origin.core.phase_math import WaveComponent, interference_score


@dataclass(frozen=True)
class ContradictionResult:
    """Contradiction index result for two competing semantic waves."""

    ci: float
    relation: str


def contradiction_index(left: WaveComponent, right: WaveComponent) -> ContradictionResult:
    """Calculate a normalized contradiction index in [0, 1]."""
    compatibility = interference_score(left, right)
    ci = (1.0 - compatibility) / 2.0
    if ci >= 0.75:
        relation = "contradictory"
    elif ci <= 0.25:
        relation = "supportive"
    else:
        relation = "ambiguous"
    return ContradictionResult(ci=ci, relation=relation)
