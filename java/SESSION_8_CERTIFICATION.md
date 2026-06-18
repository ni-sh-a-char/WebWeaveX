# SESSION 8 CERTIFICATION

**Session-crypto cluster + `json.loads` substrate.** Branch `java`. Python canon
`origin/python` @ `9625f4a` (2.1.0).

## Selection (machine-derived)

Score = (parity × reuse × blocker_reduction) ÷ substrate_cost. **session crypto = 106.7** vs
execution 12.0 / workflows 7.0 (see [`JAVA_SESSION_8_RANKING.md`](JAVA_SESSION_8_RANKING.md),
[`JAVA_SESSION_8_CLUSTER_ANALYSIS.md`](JAVA_SESSION_8_CLUSTER_ANALYSIS.md)). Chosen per the
PRIMARY RULE (eliminate future blockers) — it forces the broadly-reusable `json.loads` substrate.

## Substrate produced (the strategic deliverable)

- **`io.webweavex.determinism.PyJsonParse`** — JDK-only `json.loads` (recursive descent):
  objects→insertion-ordered maps, int→Long/BigInteger, float→Double, NaN/Infinity, `\uXXXX`
  + surrogate pairs. **100 % instruction coverage**, proven by 40 `json_loads` vectors (oracle =
  Python `json.loads`, incl. 12 malformed→raise). Reused by ~30 future `decrypt_*`/`load_*` APIs.

## Implemented APIs (4) — full cluster, no cherry-pick

| API | Java class | Python canon |
| --- | --- | --- |
| `encrypt_session_state` | `io.webweavex.crypto.KaalkaSession` | `kaalka_session_engine` |
| `decrypt_session_state` | `io.webweavex.crypto.KaalkaSession` | `kaalka_session_engine` |
| `save_encrypted_session` | `io.webweavex.session.EncryptedSessionStore` | `encrypted_session_store` |
| `load_encrypted_session` | `io.webweavex.session.EncryptedSessionStore` | `encrypted_session_store` |

No stubs/TODOs. Full audit: [`JAVA_SESSION_CRYPTO_AUDIT.md`](JAVA_SESSION_CRYPTO_AUDIT.md).

## Parity proof

- `tools/gen_java_parity_vectors_s8.py` → `golden_vectors_s8.json` — **77 vectors**:
  encrypt (12) + decrypt (12) byte-exact (stable_serialize + compute_kaalka_hash); save (6) file
  content byte-identical to Python; load (7) recovered-output byte-exact incl. missing-file;
  `json_loads` (40) substrate parity (empty/unicode/normalization/malformed/nested/mutation/
  replay/ordering/regression/boundary).
- `CrossLanguageParityS8Test` — **77/77 + corrupt-file contract test**. `mvn verify` 365/0/0.

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 27 | **31** |
| Remaining (of 128) | 101 | **97** |
| Total tests | 287 | **365** |
| Instruction coverage | 95.57% | **95.68%** (PyJsonParse 100%, EncryptedSessionStore 95%) |
| `PROVEN_FLOOR` | 27 | **31** |

## Governance & quality gates

Validator **PASS 31/128** (MAPPING +4; `session` package added to matrix PACKAGES). Matrix
regenerated. Manifest unchanged. Coverage increased; all new tests parity-backed (oracle =
Python). README counts corrected (17→31, 179→365, 94.51→95.68 %) — see
[`JAVA_README_GAP_ANALYSIS.md`](JAVA_README_GAP_ANALYSIS.md). Risk register:
[`JAVA_PARITY_RISK_REGISTER.md`](JAVA_PARITY_RISK_REGISTER.md). Extraction reality:
[`JAVA_EXTRACTION_REALITY.md`](JAVA_EXTRACTION_REALITY.md).

## Next

See [`JAVA_SESSION_9_PLAN.md`](JAVA_SESSION_9_PLAN.md): sweep the Low-risk clean clusters
(workflows/execution/synchronization/…) now that the `json.loads` blocker is removed.
