# small migration helper: ensure existing causal_graph uses compatible fields
from __future__ import annotations

from origin.graph.causal_graph import CausalGraph


def migrate_to_model_schema(graph: CausalGraph) -> None:
    """Apply lightweight migration steps so graph works with model schemas.

    This is intentionally minimal: it ensures nodes and edges expose expected
    attributes (phase, amplitude) and fills defaults.
    """
    for nid in list(graph.nodes.keys()):
        graph.nodes.setdefault(nid, {})
    for edge in graph.edges:
        if not hasattr(edge, "phase"):
            setattr(edge, "phase", 0.0)
        if not hasattr(edge, "amplitude"):
            setattr(edge, "amplitude", None)
