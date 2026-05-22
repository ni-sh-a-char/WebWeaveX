# REMOVED MODULES REPORT

**WebWeaveX v2.0.0 finalization pass**

## Policy

Modules were removed only when they were duplicate architecture trees (`v2/`, `v3/`, `experimental/`) or confirmed unreachable with zero test references.

## Removed in this pass

**None.** No `v2/`, `v3/`, or `experimental/` package directories exist at repository root. Deep audit found no abandoned parallel kernels requiring deletion without breaking the 671-test suite.

## Consolidated instead of deleted

| Area | Action |
|------|--------|
| Circular imports | Lazy `core/ir/__init__.py`, deferred parser imports |
| Parallel pipelines | Canonical path: `core/kernel/runtime_pipeline.py` |
| Volatile browser IR | `core/browser/dom_stabilization_engine.py` |
| Native simulation | Optional `core/native/platform/*` + `core/native/electron/*` |

## Candidates for future pruning (do not delete without test audit)

- Legacy `core/extract/facades/` star-import facade (still used by enrichment pipeline)
- Duplicate repository extractors (`extract_repository_v2` vs `universal_repository_extraction_engine`)
