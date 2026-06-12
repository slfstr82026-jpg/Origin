# Engine Design

The v1.0 engine keeps the implementation deliberately small and deterministic:

- `WaveEngine` collects wave components and computes a resultant phasor.
- `phase_math` normalizes phases and computes interference.
- `ContradictionResult` classifies supportive, ambiguous, and contradictory relations.
- `WaveUpdater` applies bounded evidence updates with a configurable learning rate.

Future iterations can replace these primitives with richer domain-specific embeddings while preserving the public interfaces.
