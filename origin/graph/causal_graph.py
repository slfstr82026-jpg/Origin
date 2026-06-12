"""Causal graph data model and operations (extended for learning).

This version adds a mutable 'phase' field on edges and an update_edge helper
used by the learning layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional


@dataclass
class CausalEdge:
    """A directed causal relation between two concepts.

    weight is a signed float (magnitude is strength). phase is an optional
    phase shift in radians used by the learning/phase machinery.
    """

    source: str
    target: str
    weight: float = 1.0
    label: str = "causes"
    phase: float = 0.0


@dataclass
class CausalGraph:
    """A lightweight directed weighted graph for causal reasoning."""

    nodes: Dict[str, dict] = field(default_factory=dict)
    edges: List[CausalEdge] = field(default_factory=list)

    def add_node(self, node_id: str, **attributes: object) -> None:
        """Add or update a node."""
        self.nodes.setdefault(node_id, {}).update(attributes)

    def add_edge(self, source: str, target: str, weight: float = 1.0, label: str = "causes", phase: float = 0.0) -> CausalEdge:
        """Add a directed edge, creating missing endpoint nodes."""
        self.add_node(source)
        self.add_node(target)
        edge = CausalEdge(source=source, target=target, weight=float(weight), label=label, phase=float(phase))
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

    def find_edge(self, source: str, target: str) -> Optional[CausalEdge]:
        """Return the first matching edge or None."""
        for edge in self.edges:
            if edge.source == source and edge.target == target:
                return edge
        return None

    def update_edge(self, source: str, target: str, weight: Optional[float] = None, phase: Optional[float] = None) -> Optional[CausalEdge]:
        """Update an existing edge's weight and/or phase. Returns the edge or None if missing."""
        edge = self.find_edge(source, target)
        if edge is None:
            return None
        if weight is not None:
            edge.weight = float(weight)
        if phase is not None:
            edge.phase = float(phase)
        return edge
