"""Dynamic DAG builder for question-specific causal graphs."""

from __future__ import annotations

from origin.graph.causal_graph import CausalGraph
from origin.graph.filters import filter_weak_edges
from origin.graph.subgraph_extractor import extract_subgraph


def build_question_dag(graph: CausalGraph, focus: str, depth: int = 2, threshold: float = 0.0) -> CausalGraph:
    """Build a focused acyclic view by expanding outward and dropping back edges."""
    focused = filter_weak_edges(extract_subgraph(graph, focus, depth), threshold)
    dag = CausalGraph(nodes={node: dict(attrs) for node, attrs in focused.nodes.items()})
    visited_order = {focus: 0}
    frontier = [focus]
    while frontier:
        source = frontier.pop(0)
        for edge in focused.outgoing(source):
            if edge.target not in visited_order:
                visited_order[edge.target] = len(visited_order)
                frontier.append(edge.target)
            if visited_order[source] < visited_order[edge.target]:
                dag.add_edge(edge.source, edge.target, edge.weight, edge.label)
    return dag
