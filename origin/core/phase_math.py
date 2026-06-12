"""Phase and interference mathematics for ORIGIN wave states."""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import Iterable


TAU = math.tau


@dataclass(frozen=True)
class WaveComponent:
    """A semantic wave represented by amplitude and phase in radians."""

    amplitude: float
    phase: float

    def as_complex(self) -> complex:
        """Return the phasor representation of the component."""
        return cmath.rect(self.amplitude, normalize_phase(self.phase))


def normalize_phase(phase: float) -> float:
    """Normalize a phase angle to the inclusive-exclusive range [0, 2π)."""
    return phase % TAU


def phase_distance(left: float, right: float) -> float:
    """Return the shortest angular distance between two phases."""
    delta = abs(normalize_phase(left) - normalize_phase(right))
    return min(delta, TAU - delta)


def accumulate_phase(components: Iterable[WaveComponent]) -> WaveComponent:
    """Combine wave components into a single resultant component."""
    resultant = sum((component.as_complex() for component in components), 0j)
    amplitude = abs(resultant)
    phase = normalize_phase(cmath.phase(resultant)) if amplitude else 0.0
    return WaveComponent(amplitude=amplitude, phase=phase)


def interference_score(left: WaveComponent, right: WaveComponent) -> float:
    """Return signed compatibility in [-1, 1] based on phase alignment."""
    if left.amplitude == 0 or right.amplitude == 0:
        return 0.0
    return math.cos(phase_distance(left.phase, right.phase))
