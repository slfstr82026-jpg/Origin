from origin.graph.causal_graph import CausalGraph
from origin.learning.learner import OnlineLearner
from origin.optimizer.iterative import IterativeOptimizer


def test_optimizer_improves_confidence():
    graph = CausalGraph()
    graph.add_edge("a", "b", weight=0.2)
    graph.add_edge("b", "c", weight=0.1)

    learner = OnlineLearner(learning_rate=0.5)
    optimizer = IterativeOptimizer(graph, learner, desired_confidence=0.6, max_iterations=5)

    before = optimizer._evaluate_all_pairs()
    result = optimizer.optimize()
    after = optimizer._evaluate_all_pairs()

    # Ensure optimizer ran and produced history
    assert result.iterations >= 1
    # mean confidence after should be >= before (or at least not lower)
    if before:
        assert (sum(after) / len(after)) >= (sum(before) / len(before))
