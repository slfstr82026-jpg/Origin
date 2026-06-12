"""Confidence scoring for causal explanations."""

from __future__ import annotations

from typing import Iterable

from origin.graph.causal_graph import CausalEdge


def path_confidence(edges: Iterable[CausalEdge]) -> float:
    """Compute multiplicative confidence across a path of weighted edges."""
    confidence = 1.0
    used = False
    for edge in edges:
        confidence *= max(0.0, min(abs(edge.weight), 1.0))
        used = True
    return confidence if used else 0.0
