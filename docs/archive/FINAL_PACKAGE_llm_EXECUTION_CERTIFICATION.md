# FINAL PACKAGE LLM EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 20 |
| PASS | 10 |
| FAIL | 10 |
| UNTESTED | 0 |
| Hash mismatches | 6 |
| State mismatches | 6 |

## Behavioral mismatches

- `core/llm/adapters/__init__.py` — barrel_export_mismatch:['list_adapters']
- `core/llm/adapters/adapter_sandbox.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/llm/adapters/anthropic_adapter.py` — output_or_state_mismatch
- `core/llm/adapters/gemini_adapter.py` — output_or_state_mismatch
- `core/llm/adapters/groq_adapter.py` — output_or_state_mismatch
- `core/llm/adapters/mistral_adapter.py` — output_or_state_mismatch
- `core/llm/adapters/ollama_adapter.py` — output_or_state_mismatch
- `core/llm/adapters/openai_adapter.py` — output_or_state_mismatch
- `core/llm/groq_adapter.py` — py=None js=os is not defined
- `core/llm/sandbox.py` — py=None js=deepcopy is not defined

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
