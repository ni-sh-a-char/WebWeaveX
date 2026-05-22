# FINAL PIPELINE UNIFICATION REPORT

**Canonical entry:** `run_canonical_pipeline()` in `core/kernel/runtime_pipeline.py`

## Flow

UniversalInput → ingestion → kind-specific extraction → RuntimeKernel phases → unified graph → pipeline_hash

## Specialized APIs (delegate to same engines)

- `extract_web` — browser engine (used inside pipeline for web kind)
- `extract_repository`, `extract_document_runtime`, `extract_multimodal`

## Deprecated paths

- Legacy `core.extract.pipeline.extract` only for generic text URLs