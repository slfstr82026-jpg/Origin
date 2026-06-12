from origin.graph.causal_graph import CausalGraph
from origin.learning.learner import OnlineLearner, Evidence


def test_online_learner_applies_updates():
    graph = CausalGraph()
    graph.add_edge("x", "y", weight=0.2, phase=0.0)

    learner = OnlineLearner(learning_rate=0.5)
    evidences = [Evidence("x", "y", weight_delta=0.4, phase_delta=1.5708)]

    learner.apply(graph, evidences)

    edge = graph.find_edge("x", "y")
    assert edge is not None
    # expected new weight = 0.2 + 0.5*0.4 = 0.4
    assert edge.weight == 0.4
    # phase updated toward pi/2 (approx)
    assert edge.phase != 0.0
