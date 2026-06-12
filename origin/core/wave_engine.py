from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from origin.graph.causal_graph import CausalGraph
from origin.core.phase_math import to_complex, complex_to_polar, normalize_phase


@dataclass
class PathContribution:
    path: List[str]
    complex_value: complex


@dataclass
class NodeResult:
    node: str
    complex_value: complex
    amplitude: float
    phase: float
    contributions: List[PathContribution]


def _edge_complex(edge) -> complex:
    """Compute complex representation for a graph edge.

    amplitude is derived from absolute weight; negative weight flips phase by pi.
    phase uses edge.phase and a sign correction for negative weight.
    """
    amp = abs(getattr(edge, "weight", 1.0))
    phase = getattr(edge, "phase", 0.0)
    if getattr(edge, "weight", 1.0) < 0:
        phase += 3.141592653589793
    phase = normalize_phase(phase)
    return to_complex(amp, phase)


def _paths_dfs(graph: CausalGraph, source: str, target: str, max_depth: int = 3) -> List[List[str]]:
    """Find simple paths from source to target up to max_depth (inclusive).

    This is a simple DFS avoiding cycles by tracking visited nodes.
    """
    results: List[List[str]] = []

    def dfs(current: str, visited: List[str]):
        if len(visited) - 1 > max_depth:
            return
        if current == target and len(visited) >= 2:
            results.append(list(visited))
            return
        for edge in graph.outgoing(current):
            if edge.target in visited:
                continue
            visited.append(edge.target)
            dfs(edge.target, visited)
            visited.pop()

    dfs(source, [source])
    return results


def _path_complex(graph: CausalGraph, path: List[str]) -> complex:
    """Compute the complex amplitude for a path as the product of edge complexes.

    Using multiplicative combination models attenuation along the path.
    """
    z = 1 + 0j
    for a, b in zip(path, path[1:]):
        edge = graph.find_edge(a, b)
        if edge is None:
            return 0 + 0j
        z *= _edge_complex(edge)
    return z


def simulate_propagation(graph: CausalGraph, source: str, max_depth: int = 3) -> Dict[str, NodeResult]:
    """Simulate wave propagation from a source node across the graph.

    Returns a mapping node -> NodeResult containing resultant complex amplitude,
    amplitude, phase, and the per-path contributions that were summed.
    """
    results: Dict[str, NodeResult] = {}
    nodes = list(graph.nodes.keys())
    for target in nodes:
        if target == source:
            continue
        paths = _paths_dfs(graph, source, target, max_depth=max_depth)
        contributions: List[PathContribution] = []
        total = 0 + 0j
        for p in paths:
            z = _path_complex(graph, p)
            contributions.append(PathContribution(path=p, complex_value=z))
            total += z
        amp, phase = complex_to_polar(total)
        results[target] = NodeResult(node=target, complex_value=total, amplitude=amp, phase=phase, contributions=contributions)
    return results
