"""Wave interference demo."""

from origin.core.wave_engine import WaveEngine


if __name__ == "__main__":
    engine = WaveEngine()
    engine.add_wave(1.0, 0.0)
    engine.add_wave(0.5, 0.2)
    print(engine.resultant())
