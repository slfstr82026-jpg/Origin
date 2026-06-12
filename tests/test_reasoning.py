import pytest

from origin.graph.causal_graph import CausalGraph
from origin.reasoning.confidence import confidence_from_cause_treatment, path_confidence
from origin.reasoning.explainer import explain_decision, explain_edge_impact, explain_path
from origin.reasoning.path_builder import build_path
from origin.reasoning.trace import trace_propagation, trace_wave_paths


def test_reasoning_path_trace_confidence_and_explanation():
    graph = CausalGraph()
    edge1 = graph.add_edge("obesity", "insulin_resistance", 0.7)
    edge2 = graph.add_edge("insulin_resistance", "high_glucose", 0.8)

    path = build_path(graph, "obesity", "high_glucose")
    confidence = path_confidence([edge1, edge2])
    explanation = explain_path(path, confidence)
    decision = explain_decision(path, confidence)
    trace = trace_propagation(graph, "obesity")

    assert path == ["obesity", "insulin_resistance", "high_glucose"]
    assert confidence == pytest.approx(0.56)
    assert "obesity → insulin_resistance → high_glucose" in explanation
    assert decision.startswith("Causal path")
    assert trace[0].strength == 0.7
    assert trace[0].phase == 0.0
    assert "obesity causes insulin_resistance" in explain_edge_impact(edge1)


def test_confidence_can_be_adjusted_by_scientific_contradiction_and_trace_paths():
    graph = CausalGraph()
    edge = graph.add_edge("policy", "risk", 0.8, "prevents")

    assert confidence_from_cause_treatment([edge], e_treat=0.8, e_cause=0.8) == pytest.approx(0.8)
    assert trace_wave_paths(graph, "policy") == ["policy → risk"]
