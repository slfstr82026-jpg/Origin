# API Reference

## POST `/reason`

Request body:

```json
{"question": "What causes glucose?"}
```

Response body:

```json
{
  "answer": "Causal path: glucose. Confidence: 1.00.",
  "confidence": 1.0,
  "path": ["glucose"]
}
```
