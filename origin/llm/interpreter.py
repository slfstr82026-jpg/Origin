"""LLM integration placeholder for converting questions into causal queries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CausalQuery:
    """Structured causal query inferred from user text."""

    focus: str
    target: str | None = None
    intent: str = "graph_query"


def interpret_question(question: str) -> CausalQuery:
    """Interpret a plain question as a minimal causal query."""
    tokens = [part.strip(" ?.!,;:").lower() for part in question.split() if part.strip(" ?.!,;:")]
    if not tokens:
        return CausalQuery(focus="unknown")
    if "to" in tokens and tokens.index("to") + 1 < len(tokens):
        return CausalQuery(focus=tokens[0], target=tokens[tokens.index("to") + 1], intent="causal_path")
    return CausalQuery(focus=tokens[-1])
