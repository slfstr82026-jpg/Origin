"""Contradiction index demo."""

import math

from origin.core.contradiction import contradiction_index
from origin.core.phase_math import WaveComponent


if __name__ == "__main__":
    print(contradiction_index(WaveComponent(1.0, 0.0), WaveComponent(1.0, math.pi)))
