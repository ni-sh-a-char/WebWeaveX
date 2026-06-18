# JAVA_SESSION_9_CERTIFICATION_AUDIT

**Phase 0 — repository state rebuilt from scratch (no trust of prior outputs).** All values
below are regenerated/executed live at certification time. Branch `java`, HEAD `0ecb354`.

## Rebuilt artifacts

| Artifact | Command | Result |
| --- | --- | --- |
| Parity matrix | `python tools/gen_java_parity_matrix.py` | wrote `java/JAVA_PARITY_MATRIX.md` (128 APIs, **37** Java-proven) — **no content diff** vs committed (no drift) |
| Validator report | `python tools/validate_java_manifest.py` | **PASS — 37/128 APIs proven; mapped/exist/tested/documented; README Java-native; source↔matrix consistent** |
| Test report | `mvn clean verify` | **Tests run: 454, Failures: 0, Errors: 0, Skipped: 0 — BUILD SUCCESS** |
| Coverage report | JaCoCo (`target/site/jacoco/jacoco.csv`) | **95.88 %** instruction (16421 / 17127) |

## Working tree / remote

| Check | Value |
| --- | --- |
| Branch | `java` |
| HEAD | `0ecb354` |
| Working tree | clean (`git status --porcelain` empty) |
| `HEAD == origin/java` | **yes** (pushed) |
| `PROVEN_FLOOR` | 37 |

## Matrix drift check

`gen_java_parity_matrix.py` re-run produced **no content change** to
`java/JAVA_PARITY_MATRIX.md` → matrix is consistent with the manifest + validator MAPPING
(validator checks 5 & 10 PASS).

All four rebuilt artifacts agree on **37 proven APIs** and a green suite. Proceed to per-phase
proofs.
