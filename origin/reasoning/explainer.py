"""Deterministic explanation generator."""

from __future__ import annotations

from typing import Sequence

from origin.core.contradiction import ContradictionResult
from origin.graph.causal_graph import CausalEdge


def explain_path(path: Sequence[str], confidence: float) -> str:
    """Generate a concise explanation from a causal path."""
    if not path:
        return "No supported causal path was found."
    route = " → ".join(path)
    return f"Causal path: {route}. Confidence: {confidence:.2f}."


def explain_edge_impact(edge: CausalEdge) -> str:
    """Explain the impact of one causal relation."""
    return f"{edge.source} {edge.label} {edge.target} with strength {edge.weight:.2f} and phase {edge.phase:.2f}."


def explain_decision(path: Sequence[str], confidence: float, contradiction: ContradictionResult | None = None) -> str:
    """Explain the final ORIGIN decision using path confidence and contradiction state."""
    explanation = explain_path(path, confidence)
    if contradiction and contradiction.protocol:
        return f"{explanation} Protocol: {contradiction.protocol}. {contradiction.message}"
    if contradiction:
        return f"{explanation} CI: {contradiction.ci:.2f}; relation: {contradiction.relation}."
    return explanation
