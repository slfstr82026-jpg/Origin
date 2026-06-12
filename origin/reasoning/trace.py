"""Wave propagation tracing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from origin.graph.causal_graph import CausalGraph


@dataclass(frozen=True)
class TraceStep:
    """One propagation event across a causal edge."""

    source: str
    target: str
    strength: float


def trace_propagation(graph: CausalGraph, start: str, initial_strength: float = 1.0) -> List[TraceStep]:
    """Trace one-hop propagation from a start node."""
    return [
        TraceStep(edge.source, edge.target, initial_strength * edge.weight)
        for edge in graph.outgoing(start)
    ]
