"""API schemas for ORIGIN."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EdgeInput(BaseModel):
    """Input schema for a causal edge."""

    source: str
    target: str
    weight: float = 1.0
    label: str = "causes"
    evidence: float = 1.0


class GraphQueryRequest(BaseModel):
    """Input payload for graph queries."""

    focus: str = Field(..., min_length=1)
    depth: int = Field(2, ge=1, le=10)
    threshold: float = Field(0.0, ge=0.0)
    edges: list[EdgeInput] = Field(default_factory=list)


class GraphQueryResponse(BaseModel):
    """Output payload for graph queries."""

    nodes: list[str]
    edges: list[EdgeInput]


class WaveSimulationRequest(BaseModel):
    """Input payload for wave propagation simulation."""

    start: str = Field(..., min_length=1)
    depth: int = Field(3, ge=1, le=10)
    edges: list[EdgeInput] = Field(default_factory=list)


class WaveSimulationResponse(BaseModel):
    """Output payload for wave propagation simulation."""

    arrivals: dict[str, dict[str, float | str]]
    paths: list[list[str]]


class ContradictionRequest(BaseModel):
    """Input payload for scientific contradiction analysis."""

    e_treat: float
    e_cause: float
    destructive: bool = False


class ContradictionResponse(BaseModel):
    """Output payload for contradiction analysis."""

    ci: float
    protocol: str | None


class ReasonRequest(BaseModel):
    """Input payload for causal reasoning."""

    question: str = Field(..., min_length=1)


class ReasonResponse(BaseModel):
    """Output payload for causal reasoning."""

    answer: str
    confidence: float
    path: list[str]
