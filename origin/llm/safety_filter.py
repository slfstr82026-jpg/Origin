"""Safety checks that keep LLM answers grounded in causal paths."""

from __future__ import annotations

from typing import Sequence


def is_grounded(path: Sequence[str]) -> bool:
    """Return whether an answer has a non-empty causal path to cite."""
    return len(path) > 0


def enforce_grounding(answer: str, path: Sequence[str]) -> str:
    """Return an answer only when it is grounded in a causal path."""
    if is_grounded(path):
        return answer
    return "I cannot answer without a supported causal path."
