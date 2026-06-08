# FINAL GENERATED PORT VERIFICATION

**Measured:** 2026-05-29T09:03:35.754503+00:00

| Metric | Value |
|--------|-------|
| Python `core/*.py` | 1724 |
| TypeScript `src/*.ts` | 1844 |
| Generated (non-protected) | 1706 |
| Protected operational | 138 |
| Topology files present | 1724 |
| Topology files missing | 0 |
| `@ts-nocheck` in sample (200) | 200 |

## Verdict

**Generated port behavioral equivalence: NOT PROVEN**

Run `npm run validate:differential` for executable cross-language probes.

```json
{
  "measured_at": "2026-05-29T09:03:35.754503+00:00",
  "python_modules": 1724,
  "typescript_modules": 1844,
  "generated_modules": 1706,
  "protected_modules": 138,
  "topology_present": 1724,
  "topology_missing": 0,
  "sample_nocheck_in_first_200_generated": 200,
  "execution_equivalence_proven": false,
  "execution_samples_passed": 0,
  "execution_samples_failed": 0,
  "behavioral_equivalence": "NOT PROVEN \u2014 topology only; per-module execution compare not complete"
}
```
