import math

import pytest

from origin.core.contradiction import contradiction_index, scientific_contradiction_index, scientific_contradiction_protocol
from origin.core.phase_math import WaveComponent
from origin.core.wave_engine import PropagatedWave, WaveEngine
from origin.graph.causal_graph import CausalGraph
from origin.knowledge.representation import relation_phase


def test_wave_engine_accumulates_aligned_waves():
    engine = WaveEngine()
    engine.add_wave(1.0, 0.0)
    engine.add_wave(1.0, 0.0)

    result = engine.resultant()

    assert result.amplitude == 2.0
    assert result.phase == 0.0
    assert engine.coherence() == 1.0


def test_relation_phase_mapping_and_wave_propagation():
    graph = CausalGraph()
    graph.add_edge("drug", "symptom", 0.5, "treats")
    engine = WaveEngine()

    waves = engine.propagate(graph, "drug")

    assert relation_phase("treats") == math.pi
    assert waves[0].component.amplitude == 0.5
    assert waves[0].component.phase == math.pi


def test_scientific_contradiction_protocol_detects_balanced_destructive_evidence():
    ci = scientific_contradiction_index(0.8, 0.8)
    result = contradiction_index(WaveComponent(0.8, 0.0), WaveComponent(0.8, math.pi))

    assert ci == 0.0
    assert scientific_contradiction_protocol(ci) == "SCIENTIFIC_CONTRADICTION"
    assert result.protocol == "SCIENTIFIC_CONTRADICTION"
    assert result.relation == "research_gap"


def test_interference_classifies_destructive_arrivals():
    engine = WaveEngine()
    arrivals = [
        ("target", WaveComponent(1.0, 0.0), ("a", "target")),
        ("target", WaveComponent(1.0, math.pi), ("b", "target")),
    ]
    propagated = [PropagatedWave(*arrival) for arrival in arrivals]

    result = engine.interfere(propagated)[0]

    assert result.node_id == "target"
    assert result.mode == "destructive"
    assert result.resultant.amplitude == pytest.approx(0.0)
