"""Human-facing answer rendering layer."""

from __future__ import annotations

from origin.llm.safety_filter import enforce_grounding


def render_answer(explanation: str, path: list[str] | None = None) -> str:
    """Render an explanation in a grounded user-facing form."""
    return enforce_grounding(explanation, path or [])
