# System Architecture Blueprint

ORIGIN is a multi-layer architecture that combines causal knowledge representation, wave mathematics, dynamic DAG construction, explainable reasoning, hybrid LLM grounding, APIs, and applications.

## 1. Knowledge Representation Layer

This is the foundation of ORIGIN. Concepts are modeled as knowledge nodes, and each causal relation is a wave propagation path. Relation strength becomes wave amplitude, while relation type becomes phase:

- cause: `0`
- prevent/inhibit: `-π/2`
- treat/treatment: `π`

## 2. Wave Propagation Engine

The wave engine converts relations into wave components, accumulates phase across a path with `Φ_final = Σ Δφ_i`, and combines waves algebraically when two or more paths arrive at the same node.

## 3. Interference & Contradiction Layer

The scientific contradiction index is:

```text
CI = |E_treat - E_cause| / (E_treat + E_cause)
```

When destructive or near-balanced evidence is detected, ORIGIN activates `SCIENTIFIC_CONTRADICTION` and treats the result as a research gap requiring human review.

## 4. Causal Graph Builder

This layer builds a dynamic DAG for every question by extracting causal paths, filtering weak links, estimating confidence through deterministic bootstrap-style scoring, and selecting optimal paths.

## 5. Reasoning & Explainability Layer

This layer produces the visible reasoning output: causal path, relation-level impact, final decision explanation, and confidence based on path weights and contradiction state.

## 6. Hybrid LLM Integration Layer

The LLM layer translates user questions into causal queries, renders ORIGIN results in natural language, and prevents hallucination by requiring grounded causal paths.

## 7. ORIGIN Core API Layer

The API layer exposes graph query, wave simulation, contradiction, explainability, and general reasoning endpoints.

## 8. Application Layer

ORIGIN is designed for medical diagnosis, policy analysis, cybersecurity, risk analysis, and scientific research.
