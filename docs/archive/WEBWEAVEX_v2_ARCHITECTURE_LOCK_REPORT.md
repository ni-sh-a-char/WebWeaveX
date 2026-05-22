# WEBWEAVEX v2 ARCHITECTURE LOCK REPORT

## Canonical path

`UniversalInput` → `run_canonical_pipeline()` → kernel phases → `unified_runtime_graph`

## IR flow

extraction → semantic/causality/sync → memory → execution → reconstruction → unified IR

## Kaalka

All encrypted persistence via `core.crypto.kaalka_runtime_engine`.

## Determinism

`compute_global_runtime_fingerprint()`, sorted graphs, DOM stabilization.

## Limitations

- Live dynamic SPAs may differ across separate fetches
- Native OS bindings optional