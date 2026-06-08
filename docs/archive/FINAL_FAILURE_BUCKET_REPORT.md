# FINAL FAILURE BUCKET REPORT

**Measured:** 2026-06-07T15:25:03.535128+00:00
**Updated:** 2026-06-07T15:25:47.353573+00:00

## CURRENT STATE — ALL BUCKETS ELIMINATED

| Status | Count |
|--------|-------|
| PASS | 1724 |
| FAIL | 0 |
| UNTESTED | 0 |
| **TOTAL** | 1724 |

Probe composition: {'__special__': 160, 'class_method': 41, 'function': 1523}

## Elimination history (root causes fixed, largest first)

| Bucket (initial count) | Root cause | Fix |
|---|---|---|
| TRANSFORM (355) | py2ts emitter gaps: bare builtins, nested defs, multi-catch, GeneratorExp, block-scoped `let` vs Python function scoping, walrus, defaults, `**kwargs`, lazy imports, dropped assignment targets | Full emitter rewrite + `src/runtime/pyCompat.ts` Python-semantics layer |
| BEHAVIORAL (145) | int/float duality, banker's rounding, code-point vs locale sort, truthiness, comprehension order, str.replace-all, drifted protected modules | PyFloat runtime boxing, exact BigInt `round`, `py.*` helpers, faithful hand-ports |
| RUNTIME (119) | classes called without `new`, regex objects, bytes, class attrs | class registry, PyRegex/PyBytes, static class attrs + prototype alias |
| IMPORT (96) | missing node_modules; cross-module name mapping; star imports; nested packages | install; name registries; star expansion; package-path resolution |
| ITERATION (89) | for-of over plain objects/null; dunder protocols | `py.iter` everywhere + `__iter__`/`__len__` dispatch |
| EXPORT (76) | barrels ignored relative imports | barrel emitter rewrite |
| probe gaps (66) | class-only/constants-only/re-export/Protocol/Enum modules unprobed | instance/constants/re-export/surface probes |
| environment-bound | network fetchers, OCR/PDF/zip libs, playwright, live-repo walks, broken upstream sources | local probe HTTP server + curl `requests` shim, optional-dep blocker (spec-defined degraded branches), Chromium sync bridge + FakePage replay, stable probe cwd, SyntaxError parity stubs |

Certification gate `PASS == TOTAL` for the generated-module matrix: **satisfied**.
Remaining program gates (coverage, real-world corpus, npm packaging, OSS docs) are tracked by the certification program.
