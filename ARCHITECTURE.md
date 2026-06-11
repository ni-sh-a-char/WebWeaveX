# WebWeaveX Architecture

WebWeaveX is a **universal deterministic extraction and runtime cognition
engine**, implemented three times — Python (canonical), JavaScript/TypeScript,
and Dart — with byte-identical behavior on the certified portable surface.

This document is identical across the three language repositories; only the
module-path column differs per language.

## Layer model

```
┌─────────────────────────────────────────────────────────────────┐
│  Public dispatchers                                              │
│  extract* · compile_document · compile_repository ·              │
│  query_* · reason_semantically · run_application_cognition       │
├─────────────────────────────────────────────────────────────────┤
│  IR builders                                                     │
│  Document IR · Repository IR · Runtime IR · Application IR ·     │
│  Semantic-Query IR · Knowledge IR · Graph IR                     │
├─────────────────────────────────────────────────────────────────┤
│  Cognition engines                                               │
│  semantic-IR layers A–O (≈300 functions; the core.evidence       │
│  epistemic chain) · parsers (parse_source closure) ·             │
│  application cognition · runtime cognition                       │
├─────────────────────────────────────────────────────────────────┤
│  Extraction substrate                                            │
│  bs4-parity soup engine · semantic HTML/content extraction       │
├─────────────────────────────────────────────────────────────────┤
│  Deterministic core                                              │
│  stable serialization · canonical JSON · SHA-256 hashing ·       │
│  Kaalka encryption · normalization (NFKC, volatile-key strip)    │
└─────────────────────────────────────────────────────────────────┘
```

## Module map

| Layer | Python | JavaScript | Dart |
|---|---|---|---|
| Deterministic core | `core/determinism`, `core/crypto`, `core/serialize` | `src/determinism`, `src/crypto` | `lib/src/determinism`, `lib/src/crypto` |
| Soup / extraction | `bs4` + `core/browser`, `core/extraction` | `src/runtime/pyCompat` (PySoup), `src/browser`, `src/extraction` | `lib/src/soup`, `lib/src/extraction` |
| Semantic IR (A–O) | `core/evidence`, `core/semantic`, `core/documents`, `core/graph`, `core/ast`, `core/ir` | `src/evidence`, `src/semantic`, `src/documents`, `src/graph`, `src/ast`, `src/ir` | `lib/src/semantic_ir/*` |
| Parsers | `core/parsers` | `src/parsers` | `lib/src/semantic_ir/parsers.dart` |
| Repository IR | `core/repository`, `core/ir/repository_ir.py` | `src/repository`, `src/ir/repositoryIr.ts` | `lib/src/semantic_ir/layer_repo.dart` |
| Application cognition | `core/application` | `src/application` | `lib/src/application` |
| Runtime cognition | `core/runtime*`, `core/memory`, `core/replay`, `core/reconstruction` | `src/runtime*`, `src/memory`, `src/replay` | `lib/src/{graph,memory,replay,reconstruction,kernel}*` |
| Dispatchers | `webweavex/__init__.py` | `src/index.ts` | `lib/webweavex.dart` |

## IR hierarchy

Every cognition output is an **IR** (intermediate representation): a plain
JSON-domain structure (maps, lists, strings, numbers, booleans, null) with:

- `lineage` — stage provenance
- `confidence` — score + basis, never fabricated
- `evidence` / `semantic_evidence` — what the claim rests on
- explicit boundedness flags (`bounded: true`)

IRs compose upward: `Document IR` and `Repository IR` embed the semantic-IR
epistemic chain output (`attach_epistemic_state` runs the full
humility/restraint/truth-preservation/sovereignty stack on every bundle).

## Cross-language determinism contract (v2)

- Canonical payload: JSON with code-point-sorted keys, compact separators,
  NFKC-normalized top-level strings, volatile keys stripped
  (`timestamp`, `created_at`, …).
- **Integral floats serialize as integers** (`42.0 → "42"`); non-finite → null.
  JavaScript cannot represent the int/float distinction, so the contract
  canonicalizes it away in all three languages
  (python `core/determinism/normalization.py` since `d4c5800`,
  js `048aa5c`, dart `4f4ef51`).
- Canonical hash: SHA-256 of the canonical payload —
  `compute_kaalka_hash` (py) == `computeKaalkaHash` (js) ==
  `computeDeterministicHash` (dart). Proven 60,001/60,001 on the
  10k-vector torture suite, three runs per language.
- Python sort semantics everywhere: stable sorts, code-point string
  ordering, ties-to-even rounding (`pythonRound`/`py.round`), Python float
  `repr` formatting.

## The AST contract

`parse_ast` / `compile_semantic_ast_ir`: CPython's native `ast` enriches
valid-Python sources in the Python implementation only. The certified JS/Dart
behavior is the SyntaxError fallback (`{"nodes": [], "parse_error": true}`)
with regex-path symbol extraction. The 3-way parity domain is therefore:
non-Python sources, invalid Python, and the documented scanner envelope for
`parse_python_ast`. This is a certified design boundary, not a gap.

## Portability classification

128 public APIs: **105 Complete** (parity-certified 3-way), **18 Partial**
(network/live-browser sub-paths by design: the `extract*`/`crawl*` family and
five bounded APIs), **5 Deferred** (platform-bound: live-page capture and
OS-coupled native cognition — non-deterministic across platforms even in
Python). Source of truth: `PARITY_MANIFEST.json`, regenerated from source by
`tools/dart_parity_audit.py`.
