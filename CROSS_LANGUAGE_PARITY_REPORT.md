# CROSS-LANGUAGE PARITY REPORT

**Measured:** 2026-06-08T16:53:08.938203+00:00

Python `webweavex 2.0.1` (this branch) vs JavaScript `webweavex 2.0.1` (`javascript` branch dist), measured by executing both and comparing outputs byte-for-byte. Authority: `specification/`. Neither runtime invokes the other.

| Capability | Functions (py / js) | Status |
|------------|---------------------|--------|
| Kaalka hashing | `compute_kaalka_hash / computeKaalkaHash` | Implemented (byte-identical) |
| Deterministic fingerprint | `fingerprint / fingerprint` | Implemented (byte-identical) |
| Global runtime fingerprint | `compute_global_runtime_fingerprint / computeGlobalRuntimeFingerprint` | Implemented (byte-identical) |
| Encrypted value persistence | `encrypt_value / encryptValue` | Implemented (byte-identical) |
| Runtime graph structure | `build_runtime_graph / buildRuntimeGraph` | Implemented (byte-identical) |

## Honest scope

- The capabilities above are **measured byte-identical** (or structurally equal for graph node/edge topology) this run.
- Broader module-level equality (1724 module pairs) and the 128-name public-API mapping are tracked on the `javascript` branch (`docs/specs/implementation_equality_matrix.json` = 1724/1724 EQUAL; `api_parity_report.json` = 128/128). Those are JS-side artifacts and are referenced, not re-derived here.
- **Not claimed:** full per-function behavioral equality across all 128 public functions — only the deterministic core above is directly measured byte-for-byte in this report. The remaining functions are covered by the equivalence harness against `specification/vectors`.

**Summary:** 5/5 measured capabilities byte-identical / structurally equal; 0 divergent.
