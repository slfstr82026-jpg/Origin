from origin.graph.causal_graph import CausalGraph
from origin.core.wave_engine import simulate_propagation


def test_destructive_interference():
    g = CausalGraph()
    g.add_edge("a", "b", weight=1.0, phase=0.0)
    g.add_edge("b", "d", weight=1.0, phase=0.0)

    g.add_edge("a", "c", weight=1.0, phase=3.141592653589793)  # pi
    g.add_edge("c", "d", weight=1.0, phase=0.0)

    res = simulate_propagation(g, "a", max_depth=3)
    # both paths a->b->d and a->c->d produce complex values that cancel at d
    d = res.get("d")
    assert d is not None
    assert abs(d.amplitude) < 1e-6


def test_constructive_interference():
    g = CausalGraph()
    g.add_edge("a", "b", weight=1.0, phase=0.0)
    g.add_edge("b", "d", weight=1.0, phase=0.0)

    g.add_edge("a", "c", weight=1.0, phase=0.0)
    g.add_edge("c", "d", weight=1.0, phase=0.0)

    res = simulate_propagation(g, "a", max_depth=3)
    d = res.get("d")
    assert d is not None
    # Two in-phase paths should give amplitude near 2
    assert abs(d.amplitude - 2.0) < 1e-6
