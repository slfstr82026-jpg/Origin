import math

from origin.core.phase_math import WaveComponent
from origin.core.contradiction import contradiction_index
from origin.core.wave_engine import WaveEngine


def test_wave_engine_accumulates_aligned_waves():
    engine = WaveEngine()
    engine.add_wave(1.0, 0.0)
    engine.add_wave(1.0, 0.0)

    result = engine.resultant()

    assert result.amplitude == 2.0
    assert result.phase == 0.0
    assert engine.coherence() == 1.0


def test_contradiction_index_detects_opposition():
    result = contradiction_index(WaveComponent(1.0, 0.0), WaveComponent(1.0, math.pi))

    assert result.ci == 1.0
    assert result.relation == "contradictory"
