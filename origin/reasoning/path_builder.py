"""Causal path construction."""

from __future__ import annotations

from collections import deque
from typing import List

from origin.graph.causal_graph import CausalGraph


def build_path(graph: CausalGraph, source: str, target: str) -> List[str]:
    """Return the shortest directed path between source and target, or an empty list."""
    queue: deque[list[str]] = deque([[source]])
    seen = {source}
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == target:
            return path
        for neighbor in graph.neighbors(node):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append([*path, neighbor])
    return []
