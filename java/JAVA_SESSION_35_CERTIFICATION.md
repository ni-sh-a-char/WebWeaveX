# JAVA_SESSION_35_CERTIFICATION

**Parser-pipeline completion — pure non-epistemic engines ported + certified byte-exact.**

Date: 2026-06-27 · Branch: `java` · Continues S33 (AST foundation) + S34 (parser engines).

## What this session did

Ported the **remaining pure, non-epistemic parser sub-engines** that feed
`compile_repository_ir`'s observable output (the AST/repository cluster frontier), each certified
byte-identical to canonical Python 2.1.0:

| Engine (Python `core.parsers.*`) | Java | Substrate |
|---|---|---|
| `api_resolution_engine.resolve_api_surface` | `ParserEngines.resolveApiSurface` | regex + symbol reuse |
| `semantic_graph_engine.build_semantic_graph` | `ParserEngines.buildSemanticGraph` | pure dict/set/sort |
| `formal_parser_grounding_engine.require_parser_evidence` | `ParserEngines.requireParserEvidence` | pure dict/sum |

This brings the **pure parser surface to 11/13 engines** (S34 = 8, S35 = 3). The two not ported are
deliberate and source-justified:

- `parse_ast` — composes with the **S33 AST foundation** (CPython node walk); deferred to the
  composition session, not blocked.
- `normalize_parser_output` — emits epistemic `grounding`/`cognition` fields that are **discarded
  downstream** by `compile_repository_ir` (proven in `FRONTIER_ANALYSIS.md`, frontier reduction 1).
  Porting it would mean porting the ~2776-line `core.evidence` engine for output nobody observes.
  Correctly skipped per Phase 7 (no dead infrastructure).

## Parity gotchas captured

- **`resolve_api_surface` tuple-repr**: the 2-group route regex makes Python `re.findall` return
  tuples; `sorted(set(str(r)…))` then stringifies them as CPython tuple repr `('get', '/users')`.
  Java replicates the repr exactly (ceiling: no escaping of embedded quotes/backslashes — fine for
  route literals). `rest = bool(routes)` reads the **raw** mixed list before the set-collapse.
- **`build_semantic_graph` edge ordering**: Python sorts `(from, to)` tuple keys. Java keys a
  `TreeMap` by `"from to"` with codePoint compare — the space separator is lower than any
  identifier char, so flattened compare matches tuple compare exactly. Edge basis is always
  `"observed"` (the `"inferred"` default is dead code in the canon — replicated faithfully).
- `StableSerialize` sorts object keys, so Java insertion order is irrelevant.

## Evidence

| Metric | Value |
|---|---|
| New byte-exact vectors | **13** (`parser_vectors_s35.json`, Python oracle `tools/gen_java_parser_vectors_s35.py`) |
| Full suite | **1221 tests, 0 failures, 0 errors** |
| Instruction coverage | **94.796 %** (floor 94 %) |
| Governance | `validate_java_manifest.py` → **PASS** (110/128 proven, unchanged) |
| Surface | unchanged at **110/128** — these are reusable foundations, not a new public API |

No public-API count change: S35 is foundation work. `compile_repository` certifies once the
repository-IR composition layer (~520 L, `repository_semantic_engine` + IR assembly) lands on top of
this parser surface + the S33 AST foundation.

## Reproduce

```bash
# materialize canonical Python, regenerate vectors
git archive python core | tar -x -C <scratch>/pycanon
(cd <scratch>/pycanon && python /path/tools/gen_java_parser_vectors_s35.py \
   /path/java/src/test/resources/parity/parser_vectors_s35.json)
cd java && mvn -B -ntp clean verify          # 1221 tests + JaCoCo
python ../tools/validate_java_manifest.py     # governance gate
```

**Verdict: PASS.** Pure parser-engine surface complete and byte-exact; the AST/repository cluster
frontier is reduced to AST composition + repository-IR assembly, both scoped in `FRONTIER_ANALYSIS.md`.
