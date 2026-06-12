"""Deterministic explanation generator."""

from __future__ import annotations

from typing import Sequence


def explain_path(path: Sequence[str], confidence: float) -> str:
    """Generate a concise explanation from a causal path."""
    if not path:
        return "No supported causal path was found."
    route = " → ".join(path)
    return f"Causal path: {route}. Confidence: {confidence:.2f}."
