"""Self-Iterative Optimization loop for ORIGIN.

The optimizer runs repeated inference cycles, evaluates path confidences, and
produces Evidence signals for the OnlineLearner to update graph edges (weights
and phases). The goal is to iteratively improve the overall confidence of
inferred causal paths.

This module is intentionally synchronous and deterministic for testability.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, List, Tuple

from origin.graph.causal_graph import CausalGraph
from origin.learning.learner import OnlineLearner, Evidence
from origin.reasoning.path_builder import build_path
from origin.reasoning.confidence import path_confidence


@dataclass
class OptimizeResult:
    iterations: int
    history: List[float]


class IterativeOptimizer:
    """Run iterative optimization cycles to improve reasoning confidence.

    Parameters
    - graph: the causal graph to optimize (modified in-place)
    - learner: an OnlineLearner instance used to apply evidence updates
    - desired_confidence: target confidence for paths
    - max_iterations: maximum optimization rounds
    - early_stop: stop if improvement less than this threshold
    """

    def __init__(
        self,
        graph: CausalGraph,
        learner: OnlineLearner,
        desired_confidence: float = 0.9,
        max_iterations: int = 10,
        early_stop: float = 1e-3,
    ) -> None:
        self.graph = graph
        self.learner = learner
        self.desired_confidence = float(desired_confidence)
        self.max_iterations = int(max_iterations)
        self.early_stop = float(early_stop)

    def _edges_from_path(self, path: List[str]) -> List[object]:
        edges = []
        for a, b in zip(path, path[1:]):
            edge = self.graph.find_edge(a, b)
            if edge is not None:
                edges.append(edge)
        return edges

    def _evaluate_all_pairs(self) -> List[float]:
        # evaluate all simple pairs (source, target) present in nodes
        keys = list(self.graph.nodes.keys())
        confidences: List[float] = []
        for i, src in enumerate(keys):
            for dst in keys[i + 1 :]:
                path = build_path(self.graph, src, dst)
                if not path:
                    continue
                edges = self._edges_from_path(path)
                conf = path_confidence(edges)
                confidences.append(conf)
        return confidences

    def optimize(self) -> OptimizeResult:
        history: List[float] = []
        prev_mean = 0.0
        for iteration in range(1, self.max_iterations + 1):
            confidences = self._evaluate_all_pairs()
            mean_conf = sum(confidences) / len(confidences) if confidences else 0.0
            history.append(mean_conf)

            # early stopping check
            improvement = mean_conf - prev_mean
            if iteration > 1 and abs(improvement) < self.early_stop:
                break
            prev_mean = mean_conf

            # generate evidences for low-confidence paths
            evidences: List[Evidence] = []
            keys = list(self.graph.nodes.keys())
            for i, src in enumerate(keys):
                for dst in keys[i + 1 :]:
                    path = build_path(self.graph, src, dst)
                    if not path:
                        continue
                    edges = self._edges_from_path(path)
                    conf = path_confidence(edges)
                    if conf >= self.desired_confidence:
                        continue
                    # For each edge in the path, create a small positive evidence to
                    # increase weight and nudge phase slightly toward zero (alignment)
                    delta = (self.desired_confidence - conf) * 0.1
                    for edge in edges:
                        evidences.append(Evidence(edge.source, edge.target, weight_delta=delta, phase_delta=-edge.phase * 0.1))

            if evidences:
                self.learner.apply(self.graph, evidences)

        return OptimizeResult(iterations=len(history), history=history)
