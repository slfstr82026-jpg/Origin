"""Dynamic DAG builder for question-specific causal graphs."""

from __future__ import annotations

from dataclasses import dataclass

from origin.graph.causal_graph import CausalEdge, CausalGraph
from origin.graph.filters import filter_weak_edges
from origin.graph.subgraph_extractor import extract_subgraph
from origin.reasoning.confidence import edge_confidence


@dataclass(frozen=True)
class BootstrapEstimate:
    """Deterministic confidence estimate inspired by bootstrap aggregation."""

    edge: CausalEdge
    confidence: float


def bootstrap_edge_confidence(edge: CausalEdge, samples: int = 100) -> BootstrapEstimate:
    """Estimate edge confidence from strength and evidence without randomness."""
    confidence = edge_confidence(edge) * min(1.0, max(samples, 1) / 100.0)
    return BootstrapEstimate(edge=edge, confidence=confidence)


def build_question_dag(graph: CausalGraph, focus: str, depth: int = 2, threshold: float = 0.0) -> CausalGraph:
    """Build a focused acyclic view by expanding outward and dropping back edges."""
    focused = filter_weak_edges(extract_subgraph(graph, focus, depth), threshold)
    dag = CausalGraph()
    for node in focused.nodes.values():
        dag.add_node(node.node_id, kind=node.kind, label=node.label, **dict(node.metadata))
    visited_order = {focus: 0}
    frontier = [focus]
    while frontier:
        source = frontier.pop(0)
        for edge in focused.outgoing(source):
            if edge.target not in visited_order:
                visited_order[edge.target] = len(visited_order)
                frontier.append(edge.target)
            if visited_order[source] < visited_order[edge.target]:
                dag.add_edge(edge.source, edge.target, edge.weight, edge.label, edge.evidence)
    return dag


def optimal_outgoing_edge(graph: CausalGraph, source: str) -> CausalEdge | None:
    """Return the outgoing edge with the best confidence estimate."""
    edges = graph.outgoing(source)
    if not edges:
        return None
    return max(edges, key=lambda edge: bootstrap_edge_confidence(edge).confidence)
