# FINAL DECOUPLING REPORT

**Measured:** 2026-05-29T15:29:39.413067+00:00

**Status:** IN PROGRESS

## Principle

Python may exist for **development parity validation** only.
The published `webweavex` npm package must never invoke Python.

## Action matrix

| Location | Action | Notes |
|----------|--------|-------|
| `validation/real_world/validateRealWorld.ts` | REPLACE | Remove execSync python; use JS-only URL corpus probes |
| `validation/differential/common.ts` | REPLACE | Load vectors from specification/vectors; drop origin/python authority |
| `validation/parity/runParityValidation.ts` | REPLACE | Spec-native parity, not python_vectors.json generation |
| `tests/generated/vectorConformance.test.ts` | REPLACE | Assert source=webweavex-spec |
| `src/memory/pythonParityMemory.ts` | REPLACE | Rename to specMemory / native implementation |
| `src/reconstruction/pythonParityReconstruction.ts` | REPLACE | Spec-native reconstruction |
| `.github/workflows/nightly.yml` | REPLACE | Split JS-only nightly from dev parity workflow |
| `package.json scripts (22 python entries)` | SAFE | Dev-only; move under scripts/dev/ or document as non-runtime |

## Verified

- `src/` has **0** subprocess/Python runtime invocations (see FINAL_PYTHON_DEPENDENCY_AUDIT.md)
- `package.json` `files` publishes only `dist`, `README.md`, `LICENSE`
