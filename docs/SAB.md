# System Architecture Blueprint

ORIGIN is organized into six runtime layers:

1. **Core engine**: phase math, wave interference, semantic states, contradiction index, and learning updates.
2. **Causal graph**: directed weighted graph storage, question-specific DAG construction, subgraph extraction, and edge filtering.
3. **Reasoning**: path building, propagation traces, confidence scoring, and deterministic explanations.
4. **LLM integration**: question interpretation, human answer rendering, and grounding safety checks.
5. **API**: FastAPI schemas, route registration, and application factory.
6. **Utilities**: reusable math, logging, and configuration helpers.
