# API Reference

## POST `/graph/query`

Build a focused causal DAG from supplied edges.

## POST `/wave/simulate`

Propagate waves through supplied causal edges and return node-level interference.

## POST `/contradiction`

Calculate the scientific contradiction index and protocol state.

```json
{"e_treat": 0.8, "e_cause": 0.8, "destructive": true}
```

## POST `/explain`

Return an explainable path and confidence from a supplied graph query.

## POST `/reason`

Interpret a natural-language question into a minimal grounded causal response.
