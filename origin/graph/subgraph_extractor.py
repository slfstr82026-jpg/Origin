"""Subgraph extraction for local causal contexts."""

from __future__ import annotations

from collections import deque

from origin.graph.causal_graph import CausalGraph


def extract_subgraph(graph: CausalGraph, seed: str, depth: int = 1) -> CausalGraph:
    """Extract a breadth-first outgoing subgraph around a seed node."""
    subgraph = CausalGraph()
    queue: deque[tuple[str, int]] = deque([(seed, 0)])
    seen = {seed}
    while queue:
        node, distance = queue.popleft()
        if node in graph.nodes:
            subgraph.add_node(node, **graph.nodes[node])
        if distance >= depth:
            continue
        for edge in graph.outgoing(node):
            subgraph.add_edge(edge.source, edge.target, edge.weight, edge.label)
            if edge.target not in seen:
                seen.add(edge.target)
                queue.append((edge.target, distance + 1))
    return subgraph
