"""Graph filtering helpers."""

from __future__ import annotations

from origin.graph.causal_graph import CausalGraph


def filter_weak_edges(graph: CausalGraph, threshold: float = 0.1) -> CausalGraph:
    """Return a copy containing only edges with absolute weight above threshold."""
    filtered = CausalGraph(nodes={node: dict(attrs) for node, attrs in graph.nodes.items()})
    for edge in graph.edges:
        if abs(edge.weight) >= threshold:
            filtered.add_edge(edge.source, edge.target, edge.weight, edge.label)
    return filtered
