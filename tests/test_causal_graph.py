from origin.graph.causal_graph import CausalGraph
from origin.graph.dag_builder import bootstrap_edge_confidence, build_question_dag, optimal_outgoing_edge
from origin.graph.filters import filter_weak_edges
from origin.graph.subgraph_extractor import extract_subgraph


def test_graph_adds_wave_carrying_edges_and_neighbors():
    graph = CausalGraph()
    edge = graph.add_edge("insulin_resistance", "high_glucose", 0.8, "causes", evidence=0.9)

    assert "high_glucose" in list(graph.neighbors("insulin_resistance"))
    assert graph.incoming("high_glucose")[0].weight == 0.8
    assert edge.as_relation().wave_parameters().amplitude == 0.8


def test_subgraph_filter_dag_builder_and_optimal_edge():
    graph = CausalGraph()
    graph.add_edge("a", "b", 0.9, evidence=0.9)
    graph.add_edge("a", "c", 0.4, evidence=0.5)
    graph.add_edge("b", "d", 0.05)

    subgraph = extract_subgraph(graph, "a", depth=2)
    filtered = filter_weak_edges(subgraph, threshold=0.1)
    dag = build_question_dag(graph, "a", depth=2, threshold=0.1)
    optimal = optimal_outgoing_edge(dag, "a")

    assert len(subgraph.edges) == 3
    assert len(filtered.edges) == 2
    assert len(dag.edges) == 2
    assert optimal is not None
    assert optimal.target == "b"
    assert bootstrap_edge_confidence(optimal).confidence == 0.81
