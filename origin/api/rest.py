"""REST route registration for ORIGIN."""

from __future__ import annotations

from fastapi import APIRouter

from origin.api.schemas import (
    ContradictionRequest,
    ContradictionResponse,
    EdgeInput,
    GraphQueryRequest,
    GraphQueryResponse,
    ReasonRequest,
    ReasonResponse,
    WaveSimulationRequest,
    WaveSimulationResponse,
)
from origin.core.contradiction import scientific_contradiction_index, scientific_contradiction_protocol
from origin.core.wave_engine import WaveEngine
from origin.graph.causal_graph import CausalGraph
from origin.graph.dag_builder import build_question_dag
from origin.llm.explainer_llm import render_answer
from origin.llm.interpreter import interpret_question
from origin.reasoning.confidence import path_confidence
from origin.reasoning.explainer import explain_path
from origin.reasoning.path_builder import build_path

router = APIRouter()


def graph_from_edges(edges: list[EdgeInput]) -> CausalGraph:
    """Build an in-memory causal graph from API edge inputs."""
    graph = CausalGraph()
    for edge in edges:
        graph.add_edge(edge.source, edge.target, edge.weight, edge.label, edge.evidence)
    return graph


@router.post("/graph/query", response_model=GraphQueryResponse)
def graph_query(request: GraphQueryRequest) -> GraphQueryResponse:
    """Build and return a question-focused causal DAG."""
    dag = build_question_dag(graph_from_edges(request.edges), request.focus, request.depth, request.threshold)
    return GraphQueryResponse(
        nodes=list(dag.nodes),
        edges=[EdgeInput(source=edge.source, target=edge.target, weight=edge.weight, label=edge.label, evidence=edge.evidence) for edge in dag.edges],
    )


@router.post("/wave/simulate", response_model=WaveSimulationResponse)
def wave_simulate(request: WaveSimulationRequest) -> WaveSimulationResponse:
    """Simulate wave propagation and node-level interference."""
    graph = graph_from_edges(request.edges)
    engine = WaveEngine()
    waves = engine.propagate(graph, request.start, request.depth)
    interference = engine.interfere(waves)
    arrivals = {
        result.node_id: {
            "amplitude": result.resultant.amplitude,
            "phase": result.resultant.phase,
            "mode": result.mode,
        }
        for result in interference
    }
    return WaveSimulationResponse(arrivals=arrivals, paths=[list(wave.path) for wave in waves])


@router.post("/contradiction", response_model=ContradictionResponse)
def contradiction(request: ContradictionRequest) -> ContradictionResponse:
    """Calculate CI and the SCIENTIFIC_CONTRADICTION protocol state."""
    ci = scientific_contradiction_index(request.e_treat, request.e_cause)
    return ContradictionResponse(ci=ci, protocol=scientific_contradiction_protocol(ci, request.destructive))


@router.post("/explain", response_model=ReasonResponse)
def explain(request: GraphQueryRequest) -> ReasonResponse:
    """Explain the strongest direct path in a supplied graph query."""
    graph = graph_from_edges(request.edges)
    target = request.edges[-1].target if request.edges else request.focus
    path = build_path(graph, request.focus, target) or [request.focus]
    path_edges = [graph.edge_between(left, right) for left, right in zip(path, path[1:])]
    confidence = path_confidence(edge for edge in path_edges if edge is not None) if len(path) > 1 else 1.0
    answer = render_answer(explain_path(path, confidence), path)
    return ReasonResponse(answer=answer, confidence=confidence, path=path)


@router.post("/reason", response_model=ReasonResponse)
def reason(request: ReasonRequest) -> ReasonResponse:
    """Return a deterministic placeholder causal reasoning response."""
    query = interpret_question(request.question)
    path = [query.focus] if query.target is None else [query.focus, query.target]
    confidence = 1.0
    return ReasonResponse(answer=render_answer(explain_path(path, confidence), path), confidence=confidence, path=path)
