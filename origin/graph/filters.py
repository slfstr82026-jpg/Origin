"""Graph filtering helpers."""

from __future__ import annotations

from origin.graph.causal_graph import CausalGraph


def clone_nodes(source: CausalGraph, target: CausalGraph) -> None:
    """Copy knowledge nodes from one graph into another."""
    for node in source.nodes.values():
        target.add_node(node.node_id, kind=node.kind, label=node.label, **dict(node.metadata))


def filter_weak_edges(graph: CausalGraph, threshold: float = 0.1) -> CausalGraph:
    """Return a copy containing only edges with absolute weight above threshold."""
    filtered = CausalGraph()
    clone_nodes(graph, filtered)
    for edge in graph.edges:
        if abs(edge.weight) >= threshold:
            filtered.add_edge(edge.source, edge.target, edge.weight, edge.label, edge.evidence)
    return filtered
