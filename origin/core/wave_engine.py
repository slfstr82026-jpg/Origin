"""Wave propagation and interference engine for ORIGIN."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import DefaultDict, Iterable, List

from origin.core.phase_math import WaveComponent, accumulate_phase, interference_score, normalize_phase
from origin.graph.causal_graph import CausalEdge, CausalGraph


@dataclass(frozen=True)
class PropagatedWave:
    """A wave after moving through a causal path."""

    node_id: str
    component: WaveComponent
    path: tuple[str, ...]


@dataclass(frozen=True)
class InterferenceResult:
    """Constructive/destructive interference result at one node."""

    node_id: str
    resultant: WaveComponent
    incoming: tuple[PropagatedWave, ...]
    mode: str


@dataclass
class WaveEngine:
    """Collects semantic waves and propagates them through causal graphs."""

    components: List[WaveComponent] = field(default_factory=list)

    def add_wave(self, amplitude: float, phase: float) -> WaveComponent:
        """Add a wave and return the stored component."""
        component = WaveComponent(float(amplitude), float(phase))
        self.components.append(component)
        return component

    def extend(self, components: Iterable[WaveComponent]) -> None:
        """Add multiple components to the engine."""
        self.components.extend(components)

    def resultant(self) -> WaveComponent:
        """Return the accumulated wave state."""
        return accumulate_phase(self.components)

    def coherence(self) -> float:
        """Return average pairwise phase compatibility for stored waves."""
        if len(self.components) < 2:
            return 1.0 if self.components else 0.0
        total = 0.0
        pairs = 0
        for index, left in enumerate(self.components):
            for right in self.components[index + 1 :]:
                total += interference_score(left, right)
                pairs += 1
        return total / pairs

    def wave_from_edge(self, edge: CausalEdge, incoming: WaveComponent | None = None) -> WaveComponent:
        """Convert an edge into a propagated wave component."""
        base = incoming or WaveComponent(amplitude=1.0, phase=0.0)
        return WaveComponent(amplitude=base.amplitude * edge.weight, phase=normalize_phase(base.phase + edge.phase))

    def propagate(self, graph: CausalGraph, start: str, depth: int = 3) -> list[PropagatedWave]:
        """Propagate waves from a start node through a causal graph."""
        waves: list[PropagatedWave] = []
        queue: deque[tuple[str, WaveComponent, tuple[str, ...], int]] = deque(
            [(start, WaveComponent(1.0, 0.0), (start,), 0)]
        )
        while queue:
            node_id, component, path, distance = queue.popleft()
            if distance >= depth:
                continue
            for edge in graph.outgoing(node_id):
                propagated = self.wave_from_edge(edge, component)
                next_path = (*path, edge.target)
                waves.append(PropagatedWave(edge.target, propagated, next_path))
                queue.append((edge.target, propagated, next_path, distance + 1))
        return waves

    def interfere(self, waves: Iterable[PropagatedWave]) -> list[InterferenceResult]:
        """Combine all waves that arrive at the same node."""
        grouped: DefaultDict[str, list[PropagatedWave]] = defaultdict(list)
        for wave in waves:
            grouped[wave.node_id].append(wave)

        results: list[InterferenceResult] = []
        for node_id, incoming in grouped.items():
            resultant = accumulate_phase(wave.component for wave in incoming)
            total_amplitude = sum(wave.component.amplitude for wave in incoming)
            ratio = resultant.amplitude / total_amplitude if total_amplitude else 0.0
            mode = "constructive" if ratio >= 0.5 else "destructive"
            results.append(InterferenceResult(node_id, resultant, tuple(incoming), mode))
        return results
