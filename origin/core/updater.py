"""Learning and update utilities for semantic wave states."""

from __future__ import annotations

from dataclasses import dataclass

from origin.core.phase_math import WaveComponent, normalize_phase


@dataclass
class WaveUpdater:
    """Applies bounded updates to wave components."""

    learning_rate: float = 0.1

    def update(self, current: WaveComponent, evidence: WaveComponent) -> WaveComponent:
        """Move the current wave toward incoming evidence."""
        rate = min(max(self.learning_rate, 0.0), 1.0)
        amplitude = (1 - rate) * current.amplitude + rate * evidence.amplitude
        phase = normalize_phase((1 - rate) * current.phase + rate * evidence.phase)
        return WaveComponent(amplitude=amplitude, phase=phase)
