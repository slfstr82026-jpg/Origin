"""General mathematical utilities."""

from __future__ import annotations


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Clamp a value to the provided closed interval."""
    return max(minimum, min(maximum, value))
