"""REST route registration for ORIGIN."""

from __future__ import annotations

from fastapi import APIRouter

from origin.api.schemas import ReasonRequest, ReasonResponse
from origin.llm.interpreter import interpret_question
from origin.reasoning.explainer import explain_path

router = APIRouter()


@router.post("/reason", response_model=ReasonResponse)
def reason(request: ReasonRequest) -> ReasonResponse:
    """Return a deterministic placeholder causal reasoning response."""
    query = interpret_question(request.question)
    path = [query.focus]
    confidence = 1.0
    return ReasonResponse(answer=explain_path(path, confidence), confidence=confidence, path=path)
