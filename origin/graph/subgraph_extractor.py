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
        node_id, distance = queue.popleft()
        node = graph.nodes.get(node_id)
        if node:
            subgraph.add_node(node.node_id, kind=node.kind, label=node.label, **dict(node.metadata))
        if distance >= depth:
            continue
        for edge in graph.outgoing(node_id):
            subgraph.add_edge(edge.source, edge.target, edge.weight, edge.label, edge.evidence)
            if edge.target not in seen:
                seen.add(edge.target)
                queue.append((edge.target, distance + 1))
    return subgraph
