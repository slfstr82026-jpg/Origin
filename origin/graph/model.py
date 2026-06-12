from __future__ import annotations

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, validator
from pathlib import Path


class NodeSchema(BaseModel):
    id: str
    type: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EdgeSchema(BaseModel):
    source: str
    target: str
    weight: float = 1.0
    label: str = "causes"
    phase: float = 0.0
    amplitude: Optional[float] = None
    provenance: Optional[str] = None

    @validator("weight")
    def clamp_weight(cls, v: float) -> float:
        # keep weights within a reasonable bound
        if v > 10:
            return 10.0
        if v < -10:
            return -10.0
        return v


def nodes_to_dict(nodes: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    return {nid: NodeSchema(id=nid, **attrs).dict() for nid, attrs in nodes.items()}


def edges_to_list(edges: list) -> list:
    return [EdgeSchema(**{"source": e.source, "target": e.target, "weight": getattr(e, "weight", 1.0), "label": getattr(e, "label", "causes"), "phase": getattr(e, "phase", 0.0), "amplitude": getattr(e, "amplitude", None), "provenance": getattr(e, "provenance", None)}).dict() for e in edges]


def save_graph_json(path: Path, nodes: Dict[str, Dict[str, Any]], edges: list) -> None:
    import json

    payload = {"nodes": nodes_to_dict(nodes), "edges": edges_to_list(edges)}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
