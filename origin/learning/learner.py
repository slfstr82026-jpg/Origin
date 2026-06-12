"""Online learner that updates graph weights and edge phases based on incoming evidence."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple

from origin.graph.causal_graph import CausalGraph
from origin.core.phase_math import normalize_phase
from origin.utils.math_tools import clamp


@dataclass
class Evidence:
    source: str
    target: str
    weight_delta: float = 0.0
    phase_delta: float = 0.0


class OnlineLearner:
    """Applies simple bounded updates to CausalGraph edges using observed evidence.

    The learner performs incremental updates on edge weights and phases. This is
    intentionally small and deterministic so it can be tested and extended.
    """

    def __init__(self, learning_rate: float = 0.1, weight_min: float = -1.0, weight_max: float = 1.0):
        self.learning_rate = float(learning_rate)
        self.weight_min = weight_min
        self.weight_max = weight_max

    def apply(self, graph: CausalGraph, evidences: Iterable[Evidence]) -> None:
        """Apply a batch of evidence updates to the graph in-place."""
        for ev in evidences:
            edge = graph.find_edge(ev.source, ev.target)
            if edge is None:
                # create the edge if missing, with the delta as initial weight
                graph.add_edge(ev.source, ev.target, weight=ev.weight_delta * self.learning_rate, phase=normalize_phase(ev.phase_delta * self.learning_rate))
                continue
            # update weight
            new_weight = edge.weight + self.learning_rate * ev.weight_delta
            new_weight = clamp(new_weight, self.weight_min, self.weight_max)
            # update phase
            new_phase = normalize_phase(edge.phase + self.learning_rate * ev.phase_delta)
            graph.update_edge(ev.source, ev.target, weight=new_weight, phase=new_phase)

