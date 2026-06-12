"""Confidence scoring for causal explanations."""

from __future__ import annotations

from typing import Iterable

from origin.core.contradiction import scientific_contradiction_index
from origin.graph.causal_graph import CausalEdge


def edge_confidence(edge: CausalEdge) -> float:
    """Score one edge from relation strength and evidence support."""
    return max(0.0, min(abs(edge.weight) * abs(edge.evidence), 1.0))


def path_confidence(edges: Iterable[CausalEdge], ci: float | None = None) -> float:
    """Compute multiplicative confidence across a path of weighted edges."""
    confidence = 1.0
    used = False
    for edge in edges:
        confidence *= edge_confidence(edge)
        used = True
    if not used:
        return 0.0
    if ci is not None:
        confidence *= 1.0 - max(0.0, min(ci, 1.0))
    return confidence


def confidence_from_cause_treatment(edges: Iterable[CausalEdge], e_treat: float, e_cause: float) -> float:
    """Compute path confidence adjusted by the scientific contradiction index."""
    return path_confidence(edges, ci=scientific_contradiction_index(e_treat, e_cause))
