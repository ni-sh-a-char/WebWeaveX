# WebWeaveX — AI Agent Guide

You are an AI coding agent (Claude Code, Codex, GPT, Gemini, Cursor, Aider,
Roo, Cline, …) working on WebWeaveX. This guide makes you productive in one
read. It is identical across the three language repositories.

## What this project is

A deterministic extraction and runtime cognition engine implemented **three
times** — Python (canonical), TypeScript, Dart — with byte-identical behavior
on the certified surface. The product is the *parity*, not any single
implementation. If your change makes one language drift, it is wrong even if
its tests pass.

## Branch strategy

| Branch | Content |
|---|---|
| `python` | canonical implementation (`core/` + `webweavex/`) |
| `javascript` | TypeScript port (`src/`), partially py2ts-generated |
| `dart` | Dart port (`lib/`) + the cross-language harnesses + certifications |
| `release/*` | sanitized release candidates |

The 3-way harnesses live on the `dart` branch and execute the other two via
materialized worktrees (`git worktree add ../wwx-py python`, etc.).

## Read these before coding

- `ARCHITECTURE.md` — layer model, module map, IR hierarchy, the v2
  determinism contract, the AST contract.
- `CERTIFICATION.md` — how every claim is proven and how to re-run proofs.
- `PARITY_MANIFEST.json` — the per-API source of truth
  (Complete/Partial/Deferred + proof type).

## Determinism rules (non-negotiable)

1. No wall clock, no randomness, no uuid, no locale, no platform branching in
   portable code. Seeded LCGs only, and only in test generators.
2. All outputs live in the JSON value domain. Maps/lists/strings/numbers/
   booleans/null. No language-native exotica across module boundaries.
3. Python semantics are the contract: stable sorts, code-point string
   ordering, ties-to-even rounding (`pythonRound` / `py.round`), Python float
   `repr`, `dict.get` missing-vs-null distinction (`pyGet`), truthiness
   (`pyTruthy`), `str()` reprs for containers (`pyToStr`).
4. Integral floats canonicalize to integers in serialized/hashed output (v2
   contract). Inside engine logic, float-typed arithmetic still follows
   Python exactly.
5. Mutating engines (`apply_*` bundle mutators) mutate AND return the same
   map. Preserve aliasing: post-call mutations of a sub-dict must be visible
   everywhere Python sees them.

## Cross-language pitfalls catalogue (each cost a real debugging session)

- **Python evaluates `d[key_expr] = value_expr` RHS-first**; Dart/JS evaluate
  the key first. Sequence shared-state calls (LCGs!) explicitly.
- **`str.splitlines()` has no trailing empty element**; Dart `split` keeps
  one. Use the `_pySplitlines` helpers.
- **Dart `Set<String>.union(Set<dynamic>)` throws at runtime.** Build
  key-sets as `Set<dynamic>.of(map.keys)`.
- **Dart `List.sort` is unstable**; Python `sorted` is stable. Use
  `pyStableSortedBy` (index tie-break).
- **Python `or`/`and` return operands, not booleans.** `x or {}` /
  `a and 1.0 or 0.0` need explicit `pyTruthy` ternaries.
- **Python tuple sort**: emulate with NUL-joined keys or element-wise
  comparators, never space-joined strings.
- **Two-group `re.findall` returns tuples** whose `str()` is
  `"('a', 'b')"` — reproduce the repr exactly.
- **py2ts tuple dict-keys** coerce to `"a,b"` strings on JS objects and then
  destructure as *characters*. Re-key with JSON-encoded pairs.
- **`py.regex()` returns `PyRegex`, not `RegExp`** — `instanceof RegExp`
  misses it.
- **JSON cannot express `0.0` for JS** — fixtures with float-typed args must
  use non-integral values (0.4, not 0.0) or rely on each language's own
  default parameter.
- **bs4 `class_` matchers run per class token** (and on `None` for class-less
  tags); `attrs={...}` compares the space-joined value.
- **`merge_evidence(*parts)` is variadic** — wrap single parts in a list.
- **Keyword-only Python params** become trailing positionals in py2ts order
  in JS/Dart; harness `kwargs` maps fill defaults (float defaults must be
  PyFloat-boxed in JS).
- **Function-local imports are invisible to dependency scanners.** When
  mapping a closure, grep function bodies for `from ... import`.
- Read the WHOLE Python engine file before porting. Windowed reads have
  missed load-bearing lines (`bundle["fragility_pressure"]`).

## Workflows

### Porting an engine (Python → Dart/JS)

1. `cat` the full Python source. List every dependency; check
   `PARITY_MANIFEST.json` / existing libs for already-ported deps and their
   exact signatures.
2. Port bit-exactly using the py-compat helpers. No simplifications.
3. Register in the three harness runners
   (`validation/semantic_ir/run_*.{py,mjs,dart}`); dotted registry keys for
   name collisions.
4. Add fixtures via a `gen_*_fixtures.py` script (append to
   `fixtures.json`; branch coverage, edge cases, Python-truthiness traps).
5. Execute 3-way, `compare_results.py`. Investigate EVERY mismatch — the
   divergence is as often a JS-branch or harness bug as a port bug; Python
   is canonical.
6. Freeze vectors (`validation/parity/*_vectors.json` from executed Python),
   add the suite test, run analyzer + full tests.
7. Regenerate matrix/manifest (`tools/dart_parity_audit.py`,
   `tools/generate_parity_manifest.py`, `tools/generate_reports.py`).

### Certification re-run

See `CERTIFICATION.md`. Headline gates: semantic-IR 667/667, core
60,001/60,001, extraction 10k+1006+14, executable 35/35, million-vector
digest equality, full test suites, clean analyzers.

### Release

Release branches are sanitized snapshots (`release/<language>`). Validation
happens only from FRESH clones of the committed release branch. Never reuse a
dirty workspace as evidence.

## Coding standards

- Dart: zero-issue `dart analyze` under strict-casts/strict-inference;
  explicit type args on collection literals; `dart format`.
- Python: the canonical branch is edited only to fix genuine canonical bugs —
  with cross-language sign-off, since it moves the contract for everyone.
- TS: generated files are marked `@generated`; hand-fixed files carry a
  "Hand-fixed production module" header explaining why.
- Tests asserting parity must compare against **executed-Python** vectors,
  not hand-written expectations. When a spot-check disagrees with the vector,
  trust the vector — your mental model of Python is the thing under test.

## Common mistakes that will get your PR rejected

- Marking an API Complete without a 3-way executed proof.
- "Fixing" a parity mismatch by changing the Python side without
  understanding it (Python is the contract).
- Deleting "unused" files without reference-count evidence.
- Trusting any historical report. Re-execute it.
