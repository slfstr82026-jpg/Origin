"""Safety checks that keep answers grounded in causal paths."""

from __future__ import annotations

from typing import Sequence


def is_grounded(path: Sequence[str]) -> bool:
    """Return whether an answer has a non-empty causal path to cite."""
    return len(path) > 0
