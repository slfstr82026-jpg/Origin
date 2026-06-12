"""Causal graph data model and operations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List

from origin.knowledge.representation import KnowledgeNode, KnowledgeRelation, relation_phase


@dataclass(frozen=True)
class CausalEdge:
    """A directed causal relation between two concepts."""

    source: str
    target: str
    weight: float = 1.0
    label: str = "causes"
    evidence: float = 1.0

    @property
    def phase(self) -> float:
        """Return the wave phase associated with this edge label."""
        return relation_phase(self.label)

    def as_relation(self) -> KnowledgeRelation:
        """Return this edge as a knowledge-layer relation."""
        return KnowledgeRelation(
            source=self.source,
            target=self.target,
            relation_type=self.label,
            strength=self.weight,
            evidence=self.evidence,
        )


@dataclass
class CausalGraph:
    """A lightweight directed weighted graph for causal reasoning."""

    nodes: Dict[str, KnowledgeNode] = field(default_factory=dict)
    edges: List[CausalEdge] = field(default_factory=list)

    def add_node(self, node_id: str, kind: str = "concept", label: str | None = None, **metadata: object) -> None:
        """Add or update a knowledge node."""
        existing = self.nodes.get(node_id)
        merged = dict(existing.metadata) if existing else {}
        merged.update(metadata)
        self.nodes[node_id] = KnowledgeNode(node_id=node_id, kind=kind, label=label or node_id, metadata=merged)

    def add_edge(
        self,
        source: str,
        target: str,
        weight: float = 1.0,
        label: str = "causes",
        evidence: float = 1.0,
    ) -> CausalEdge:
        """Add a directed wave-carrying edge, creating missing endpoint nodes."""
        self.add_node(source)
        self.add_node(target)
        edge = CausalEdge(source=source, target=target, weight=float(weight), label=label, evidence=float(evidence))
        self.edges.append(edge)
        return edge

    def add_relation(self, relation: KnowledgeRelation) -> CausalEdge:
        """Add a knowledge-layer relation as a causal graph edge."""
        return self.add_edge(
            relation.source,
            relation.target,
            relation.strength,
            relation.relation_type,
            relation.evidence,
        )

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

    def edge_between(self, source: str, target: str) -> CausalEdge | None:
        """Return the first edge connecting source to target, if present."""
        for edge in self.outgoing(source):
            if edge.target == target:
                return edge
        return None
