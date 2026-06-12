# Engine Design

The ORIGIN engine is organized around the official layered architecture:

1. `origin.knowledge` defines nodes, relations, relation phases, and wave parameters.
2. `origin.core.wave_engine` propagates relation waves through causal paths and computes constructive/destructive interference at shared destination nodes.
3. `origin.core.contradiction` implements the scientific CI equation and `SCIENTIFIC_CONTRADICTION` protocol.
4. `origin.graph` builds focused DAGs, filters weak edges, and estimates edge confidence.
5. `origin.reasoning` builds paths, traces propagation, scores confidence, and explains decisions.
6. `origin.llm` keeps language-model output grounded in causal paths.
7. `origin.api` exposes the Core API layer.
8. `origin.applications` lists target application domains.
