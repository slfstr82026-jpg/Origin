"""Rule-based placeholder for converting user questions into causal queries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CausalQuery:
    """Structured causal query inferred from user text."""

    focus: str
    target: str | None = None


def interpret_question(question: str) -> CausalQuery:
    """Interpret a plain question as a minimal causal query."""
    terms = [part.strip(" ?.!").lower() for part in question.split() if part.strip(" ?.!:")]
    focus = terms[-1] if terms else "unknown"
    return CausalQuery(focus=focus)
