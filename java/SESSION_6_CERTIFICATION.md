# SESSION 6 CERTIFICATION

**Slice:** `build_interaction_graph` — the largest proven dependency-clean interaction
subsystem. Branch `java`. Python canon `origin/python` @ `9625f4a` (2.1.0).

## Phase 0 — blocker revalidation (compile_document)

[`JAVA_SESSION_6_BLOCKER_AUDIT.md`](JAVA_SESSION_6_BLOCKER_AUDIT.md) — runtime call trace
(`tools/runtime_trace_s6.py`):

| Question | Result |
| --- | --- |
| Import without bs4? | **No** (hard load-time dep) |
| Executes any bs4 path in `compile_document(text)`? | **No** — 238 core modules / 311 funcs run; 12 `core.semantic` *pressure* engines run; **0** bs4/table/ui hits |

**Verdict: A — import-time blocked only, not behavioral.** The bs4 is dead eager-package
weight. Recorded for a future canon-refactor or behavioral-gate decision; no action this session.

## Phase 1 — analysis (build_interaction_graph)

[`JAVA_SESSION_6_ANALYSIS.md`](JAVA_SESSION_6_ANALYSIS.md): relative-aware closure =
**5 modules / 326 lines / 0 forbidden**. Only **1 new module** to port
(`interaction_graph_engine.py`, 81 L); the other 4 (kaalka hash/runtime/v5, normalization) are
the Session-1 foundation, already byte-exact. No BeautifulSoup/lxml/OCR/PDF/DOCX/browser/
network/LLM. Cleared.

## Phase 2 — traceability

[`JAVA_SESSION_6_TRACEABILITY.md`](JAVA_SESSION_6_TRACEABILITY.md): `build_interaction_graph`
→ `io.webweavex.interaction.InteractionGraph#buildInteractionGraph` → `golden_vectors_s6.json`
section `build_interaction_graph` → manifest `build_interaction_graph`. Sibling
`interaction_graph_to_runtime_ir` explicitly excluded (no orphan).

## Implemented API (1)

| Manifest API | Java class | Python canon |
| --- | --- | --- |
| `build_interaction_graph` | `io.webweavex.interaction.InteractionGraph#buildInteractionGraph` | `core.interaction.interaction_graph_engine.build_interaction_graph` |

No stubs/TODOs/placeholders. Embedded `graph_hash` uses the certified
`Kaalka.computeKaalkaHash` (= `compute_kaalka_hash_payload` = `sha256(stable_serialize)`).

## Parity proof

- Generator: `tools/gen_java_parity_vectors_s6.py` (imports canonical `core`).
- Vectors: `java/src/test/resources/parity/golden_vectors_s6.json` — **20** vectors covering
  empty graph, single interaction (every relation/type branch), multiple interactions,
  malformed (missing/extra keys, int/None id), cyclic (repeated node ids), Unicode (CJK/emoji/
  accent), NFKC normalization (ligature + trailing whitespace), ordering (a·b vs b·a), and a
  realistic replay log.
- Test: `io.webweavex.parity.CrossLanguageParityS6Test` — every vector asserts
  `stable_serialize` **and** `compute_kaalka_hash` byte-equal to recorded Python.
- Result: **20/20 byte-exact**.

## Counts

| Metric | Before (S4B) | After (S6) |
| --- | --- | --- |
| Parity-proven manifest APIs | 23 | **24** |
| Remaining (of 128) | 105 | **104** |
| Total tests | 249 | **269** (+20 parity) |
| Instruction coverage | 95.37% | **95.45%** (InteractionGraph 99.19%) |

## Governance

- `tools/validate_java_manifest.py` — `MAPPING` +1 → **PASS 24/128** (all 10 checks).
- `java/JAVA_PARITY_MATRIX.md` — regenerated; **24** proven (no manual counting).
- `.github/workflows/parity-regression.yml` — `PROVEN_FLOOR` 23 → **24**; coverage floor 94%
  (now 95.45%).
- `PARITY_MANIFEST.json` — **not modified**.

## Quality gates

Coverage increased (95.37% → 95.45%). All new tests are **parity-backed** (Python-generated
vectors); no synthetic / self-consistency tests added. `mvn verify` BUILD SUCCESS (269/0/0).
Validator PASS. No forbidden-dependency shim in `src/main`.
