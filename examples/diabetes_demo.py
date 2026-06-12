"""Minimal diabetes causal-path demo."""

from origin.graph.causal_graph import CausalGraph
from origin.reasoning.confidence import path_confidence
from origin.reasoning.explainer import explain_decision
from origin.reasoning.path_builder import build_path


def run() -> str:
    graph = CausalGraph()
    edges = [
        graph.add_edge("insulin_resistance", "high_glucose", 0.85, "causes"),
        graph.add_edge("high_glucose", "diabetes_risk", 0.9, "causes"),
    ]
    path = build_path(graph, "insulin_resistance", "diabetes_risk")
    return explain_decision(path, path_confidence(edges))


if __name__ == "__main__":
    print(run())
