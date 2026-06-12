from __future__ import annotations

import math
import cmath
from typing import Tuple


def normalize_phase(phase: float) -> float:
    """Normalize phase to the range (-pi, pi]."""
    p = math.fmod(phase + math.pi, 2 * math.pi)
    if p < 0:
        p += 2 * math.pi
    return p - math.pi


def to_complex(amplitude: float, phase: float) -> complex:
    """Convert polar representation to complex number.

    amplitude: non-negative scalar
    phase: radians
    """
    return cmath.rect(float(amplitude), float(phase))


def complex_to_polar(z: complex) -> Tuple[float, float]:
    """Return (amplitude, phase) given a complex number. Phase normalized."""
    amp = abs(z)
    phase = math.atan2(z.imag, z.real)
    return amp, normalize_phase(phase)
