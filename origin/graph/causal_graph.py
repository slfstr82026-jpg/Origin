"""Causal graph data model and operations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class CausalEdge:
    """A directed causal relation between two concepts."""

    source: str
    target: str
    weight: float = 1.0
    label: str = "causes"


@dataclass
class CausalGraph:
    """A lightweight directed weighted graph for causal reasoning."""

    nodes: Dict[str, dict] = field(default_factory=dict)
    edges: List[CausalEdge] = field(default_factory=list)

    def add_node(self, node_id: str, **attributes: object) -> None:
        """Add or update a node."""
        self.nodes.setdefault(node_id, {}).update(attributes)

    def add_edge(self, source: str, target: str, weight: float = 1.0, label: str = "causes") -> CausalEdge:
        """Add a directed edge, creating missing endpoint nodes."""
        self.add_node(source)
        self.add_node(target)
        edge = CausalEdge(source=source, target=target, weight=float(weight), label=label)
        self.edges.append(edge)
        return edge

    def outgoing(self, node_id: str) -> List[CausalEdge]:
        """Return outgoing edges for a node."""
        return [edge for edge in self.edges if edge.source == node_id]

    def incoming(self, node_id: str) -> List[CausalEdge]:
        """Return incoming edges for a node."""
        return [edge for edge in self.edges if edge.target == node_id]

    def neighbors(self, node_id: str) -> Iterable[str]:
        """Yield outgoing neighbor node identifiers."""
        for edge in self.outgoing(node_id):
            yield edge.target
