"""Wave propagation tracing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from origin.core.wave_engine import WaveEngine
from origin.graph.causal_graph import CausalGraph


@dataclass(frozen=True)
class TraceStep:
    """One propagation event across a causal edge."""

    source: str
    target: str
    strength: float
    phase: float
    relation: str


def trace_propagation(graph: CausalGraph, start: str, initial_strength: float = 1.0) -> List[TraceStep]:
    """Trace one-hop propagation from a start node."""
    return [
        TraceStep(edge.source, edge.target, initial_strength * edge.weight, edge.phase, edge.label)
        for edge in graph.outgoing(start)
    ]


def trace_wave_paths(graph: CausalGraph, start: str, depth: int = 3) -> list[str]:
    """Return human-readable wave propagation paths."""
    engine = WaveEngine()
    return [" → ".join(wave.path) for wave in engine.propagate(graph, start, depth)]
