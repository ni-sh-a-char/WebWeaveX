# JAVA_SESSION_6_TRACEABILITY

**Phase 2 — Python → Java → parity-vector → manifest traceability for
`build_interaction_graph`. 100% coverage, no orphans.**

## Public API

| Python source | Java target | Parity-vector section | Manifest API |
| --- | --- | --- | --- |
| `core.interaction.interaction_graph_engine.build_interaction_graph` | `io.webweavex.interaction.InteractionGraph#buildInteractionGraph` | `golden_vectors_s6.json` → `build_interaction_graph` | `build_interaction_graph` (Complete) |

## Supporting functions / primitives (already byte-exact in Java — not re-ported)

| Python source | Java target | Status |
| --- | --- | --- |
| `core.crypto.kaalka_hash_engine.compute_kaalka_hash_payload` (= `compute_deterministic_hash` = `sha256(stable_serialize)`) | `io.webweavex.crypto.Kaalka#computeKaalkaHash` | Session 1 (parity-proven) |
| `core.determinism.normalization.stable_serialize` | `io.webweavex.determinism.StableSerialize#stableSerialize` | Session 1 (parity-proven) |
| `core.crypto.kaalka_v5_proc`, `kaalka_runtime_engine` | `io.webweavex.crypto.KaalkaV5Proc`, `Kaalka` | Session 1 (parity-proven) |

## Explicitly out of scope (no orphan — intentionally excluded)

| Python source | Reason |
| --- | --- |
| `core.interaction.interaction_graph_engine.interaction_graph_to_runtime_ir` | Sibling function in the same module; **not** the `build_interaction_graph` API. Mission: "Port `build_interaction_graph` only. Do not port siblings." |

## Coverage statement

The single in-scope public function `build_interaction_graph` maps 1:1 to one Java method, one
golden-vector section, and one manifest API. Every helper it calls is an already-proven
foundation primitive. **No function in the in-scope closure is left without a Java target and a
parity vector.**
