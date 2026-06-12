"""API schemas for ORIGIN."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ReasonRequest(BaseModel):
    """Input payload for causal reasoning."""

    question: str = Field(..., min_length=1)


class ReasonResponse(BaseModel):
    """Output payload for causal reasoning."""

    answer: str
    confidence: float
    path: list[str]
