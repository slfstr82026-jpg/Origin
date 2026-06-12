"""Wave interference engine for semantic evidence propagation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List

from origin.core.phase_math import WaveComponent, accumulate_phase, interference_score


@dataclass
class WaveEngine:
    """Collects semantic waves and computes their resultant interference."""

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
