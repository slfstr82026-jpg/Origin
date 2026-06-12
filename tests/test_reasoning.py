import pytest

from origin.graph.causal_graph import CausalGraph
from origin.reasoning.confidence import path_confidence
from origin.reasoning.explainer import explain_path
from origin.reasoning.path_builder import build_path
from origin.reasoning.trace import trace_propagation


def test_reasoning_path_trace_confidence_and_explanation():
    graph = CausalGraph()
    edge1 = graph.add_edge("obesity", "insulin_resistance", 0.7)
    edge2 = graph.add_edge("insulin_resistance", "high_glucose", 0.8)

    path = build_path(graph, "obesity", "high_glucose")
    confidence = path_confidence([edge1, edge2])
    explanation = explain_path(path, confidence)
    trace = trace_propagation(graph, "obesity")

    assert path == ["obesity", "insulin_resistance", "high_glucose"]
    assert confidence == pytest.approx(0.56)
    assert "obesity → insulin_resistance → high_glucose" in explanation
    assert trace[0].strength == 0.7
