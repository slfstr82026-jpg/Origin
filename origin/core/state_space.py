"""Semantic state-space primitives for ORIGIN."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, Mapping


@dataclass
class SemanticState:
    """A sparse weighted semantic vector."""

    weights: Dict[str, float] = field(default_factory=dict)

    def normalized(self) -> "SemanticState":
        """Return a unit-length copy of this semantic state."""
        norm = math.sqrt(sum(value * value for value in self.weights.values()))
        if norm == 0:
            return SemanticState(dict(self.weights))
        return SemanticState({key: value / norm for key, value in self.weights.items()})

    def similarity(self, other: "SemanticState") -> float:
        """Compute cosine similarity with another semantic state."""
        left = self.normalized().weights
        right = other.normalized().weights
        keys = set(left) | set(right)
        return sum(left.get(key, 0.0) * right.get(key, 0.0) for key in keys)

    @classmethod
    def from_mapping(cls, values: Mapping[str, float]) -> "SemanticState":
        """Create a state from any string-to-number mapping."""
        return cls({key: float(value) for key, value in values.items()})
