# ORIGIN

ORIGIN is a wave-based causal reasoning toolkit. Version 1.0 establishes the official project skeleton, core mathematical primitives, causal graph utilities, reasoning helpers, LLM integration placeholders, and a FastAPI interface.

## Project layout

```text
origin/
├── origin/       # Python package
├── data/         # graph store, wave states, and logs
├── tests/        # pytest suite
├── docs/         # architecture and API documentation
└── examples/     # runnable demos
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn origin.api.server:app --reload
```

## API

POST `/reason` with a JSON payload:

```json
{"question": "What causes glucose?"}
```

The current v1.0 endpoint returns a deterministic grounded placeholder response while the causal store and learning pipeline evolve.

## تشغيل المشروع واختباراته

1. إنشاء بيئة افتراضية وتفعيلها:
   - python -m venv .venv
   - source .venv/bin/activate  (macOS / Linux)
   - .\.venv\Scripts\activate  (Windows)

2. تثبيت الاعتمادات:
   - pip install -r requirements.txt

3. تشغيل الاختبارات:
   - pytest

4. تشغيل الخادم (local):
   - uvicorn origin.api.server:app --reload
