# ORIGIN

ORIGIN is a layered hybrid reasoning system that combines knowledge representation, wave propagation mathematics, dynamic causal DAG building, explainable reasoning, LLM integration, Core APIs, and application-domain adapters.

The v1.0 architecture is intentionally deterministic: every answer should be grounded in causal nodes, relation phases, wave interference, contradiction analysis, and an explainable path.

## Official architecture layers

1. **Knowledge Representation Layer**: concepts are nodes; causal relations are typed, weighted, evidence-backed wave paths.
2. **Wave Propagation Engine**: relations become complex waves with amplitude and phase; paths accumulate phase and interfere at shared nodes.
3. **Interference & Contradiction Layer**: scientific contradiction is measured with `CI = |E_treat - E_cause| / (E_treat + E_cause)` and can activate `SCIENTIFIC_CONTRADICTION`.
4. **Causal Graph Builder**: builds question-specific DAGs, filters weak links, estimates confidence, and selects optimal causal edges.
5. **Reasoning & Explainability Layer**: builds causal paths, traces propagation, scores confidence, and explains final decisions.
6. **Hybrid LLM Integration Layer**: interprets questions, renders human-readable explanations, and blocks ungrounded answers.
7. **ORIGIN Core API Layer**: exposes graph query, wave simulation, contradiction, explainability, and reasoning endpoints.
8. **Application Layer**: targets medical AI, policy analysis, cybersecurity, risk analysis, and scientific research.

## Structured diagram

```text
┌──────────────────────────────────────────────┐
│                Application Layer             │
│  (Medical AI, Policy, Cybersecurity, R&D)    │
└──────────────────────────────────────────────┘
                     ▲
┌──────────────────────────────────────────────┐
│              ORIGIN Core API Layer           │
│  (Graph API, Wave API, Contradiction API)    │
└──────────────────────────────────────────────┘
                     ▲
┌──────────────────────────────────────────────┐
│        Reasoning & Explainability Layer      │
│   (Path Builder, Confidence, Interpretation) │
└──────────────────────────────────────────────┘
                     ▲
┌──────────────────────────────────────────────┐
│        Causal Graph Builder (DAG Engine)     │
│   (Filtering, Bootstrap, Optimal Path)       │
└──────────────────────────────────────────────┘
                     ▲
┌──────────────────────────────────────────────┐
│   Wave Propagation & Interference Engine     │
│ (Phase Accumulation, Constructive/Destructive)│
└──────────────────────────────────────────────┘
                     ▲
┌──────────────────────────────────────────────┐
│        Knowledge Representation Layer        │
│ (Nodes, Relations, Wave Parameters, Semantics)│
└──────────────────────────────────────────────┘
                     ▲
┌──────────────────────────────────────────────┐
│        Hybrid LLM Integration Layer          │
│ (Interpreter, Explainer, Safety Filter)      │
└──────────────────────────────────────────────┘
```

## Relation phase mapping

| Relation | Phase |
| --- | --- |
| causes | `0` |
| prevents / inhibits | `-π/2` |
| treats / treatment | `π` |

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn origin.api.server:app --reload
```

## Core APIs

- `POST /graph/query`
- `POST /wave/simulate`
- `POST /contradiction`
- `POST /explain`
- `POST /reason`
