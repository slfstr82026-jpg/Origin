from origin.graph.causal_graph import CausalGraph
from origin.graph.dag_builder import build_question_dag
from origin.graph.filters import filter_weak_edges
from origin.graph.subgraph_extractor import extract_subgraph


def test_graph_adds_edges_and_neighbors():
    graph = CausalGraph()
    graph.add_edge("insulin_resistance", "high_glucose", 0.8)

    assert "high_glucose" in list(graph.neighbors("insulin_resistance"))
    assert graph.incoming("high_glucose")[0].weight == 0.8


def test_subgraph_filter_and_dag_builder():
    graph = CausalGraph()
    graph.add_edge("a", "b", 0.9)
    graph.add_edge("b", "c", 0.05)

    subgraph = extract_subgraph(graph, "a", depth=2)
    filtered = filter_weak_edges(subgraph, threshold=0.1)
    dag = build_question_dag(graph, "a", depth=2, threshold=0.1)

    assert len(subgraph.edges) == 2
    assert len(filtered.edges) == 1
    assert len(dag.edges) == 1
