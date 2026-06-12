"""Knowledge representation primitives for ORIGIN.

This layer models concepts as nodes and causal links as wave-carrying
relations. Each relation is converted into wave parameters where amplitude is
the relation strength and phase encodes the relation type.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Mapping


RELATION_PHASES: dict[str, float] = {
    "causes": 0.0,
    "cause": 0.0,
    "prevents": -math.pi / 2,
    "inhibits": -math.pi / 2,
    "treats": math.pi,
    "treatment": math.pi,
}


@dataclass(frozen=True)
class KnowledgeNode:
    """A concept in the ORIGIN knowledge layer."""

    node_id: str
    kind: str = "concept"
    label: str | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class WaveParameters:
    """Wave parameters attached to a causal relation."""

    amplitude: float
    phase: float


@dataclass(frozen=True)
class KnowledgeRelation:
    """A causal relation represented as a wave propagation path."""

    source: str
    target: str
    relation_type: str = "causes"
    strength: float = 1.0
    evidence: float = 1.0

    def wave_parameters(self) -> WaveParameters:
        """Convert this relation into amplitude and phase parameters."""
        return WaveParameters(amplitude=float(self.strength), phase=relation_phase(self.relation_type))


def relation_phase(relation_type: str) -> float:
    """Return the phase shift associated with a relation type."""
    return RELATION_PHASES.get(relation_type.lower(), 0.0)
