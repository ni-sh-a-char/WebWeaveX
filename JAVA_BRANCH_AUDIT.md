# JAVA_BRANCH_AUDIT

**Phase 1 deliverable — structural audit of the `java` branch.**

Machine-readable companion: [`JAVA_BRANCH_AUDIT.json`](JAVA_BRANCH_AUDIT.json),
regenerated deterministically by [`tools/audit_java_branch.py`](tools/audit_java_branch.py)
(`python tools/audit_java_branch.py`). No source was modified to produce this audit.

## Why this audit exists

The `java` branch was forked from the multi-language line and therefore still
carries the **entire Dart source tree, the Dart/JS/Python certification harnesses,
and Dart/JS/Python build & release artifacts** alongside the real Maven project in
`java/`. The mission is two invariants held at once:

```
Python  =  Java  =  JavaScript  =  Dart        (behavioural parity)
AND
each branch looks native to its own ecosystem   (structural identity)
```

Today the first holds (for the 17 proven APIs); the second does **not** — the
branch root reads as a Dart/pub package, not a Maven project.

## Method

Every git-tracked file (`git ls-files`, **623 files**) is classified by rule into
exactly one of six categories and assigned a cleanup disposition. The classifier is
deterministic and reproducible; re-running it reproduces `JAVA_BRANCH_AUDIT.json`
byte-for-byte.

## Results

### By category

| Category | Files | Meaning |
| --- | ---: | --- |
| `required_java` | **74** | Maven build, Java parity generators/validator, Java CI, `PARITY_MANIFEST.json` |
| `shared_governance` | **97** | Language-neutral governance + cross-language reference docs |
| `legacy_dart` | **273** | Dart-ecosystem artifacts (belong on the `dart` branch) |
| `legacy_python` | **169** | Python / multi-language artifacts (belong on `python`) |
| `legacy_js` | **10** | JavaScript-ecosystem artifacts (belong on `javascript`) |
| `unknown` | **0** | — every file classified by rule |
| **Total** | **623** | |

### By disposition

| Disposition | Files | Action |
| --- | ---: | --- |
| `keep` | **170** | Stays on the Java branch as-is |
| `rewrite` | **1** | `README.md` → rewritten Java-native (Phase 3) |
| `relocate` | **7** | Moved under `docs/archive/` (Phase 2) |
| `remove` | **445** | Deleted from the Java branch — preserved in git history and on the sibling `dart`/`python`/`javascript` branches (Phase 2) |

### By location × category

| Location | Category | Files |
| --- | --- | ---: |
| `java/` | required_java | 64 |
| `tools/` | required_java | 6 |
| `tools/` | legacy_python | 11 |
| `.github/` | required_java | 3 |
| `.github/` | shared_governance | 6 |
| `.github/` | legacy_dart (`dart.yml`) | 1 |
| `.github/` | legacy_python (`ci.yml`) | 1 |
| `docs/` | shared_governance | 72 |
| `lib/` | legacy_dart | 191 |
| `test/` | legacy_dart | 56 |
| `example/` | legacy_dart | 1 |
| `validation/` | legacy_dart / js / python | 13 / 4 / 98 |
| `cross_language_verifier/` | legacy_dart / js / python | 6 / 5 / 48 |
| `(root)` | shared_governance | 19 |
| `(root)` | required_java (`PARITY_MANIFEST.json`) | 1 |
| `(root)` | legacy_dart / js / python | 5 / 1 / 11 |

## Category 1 — Required for Java (74, all `keep`)

- **`java/**` (64)** — the Maven project: `pom.xml`, `src/main/java/io/webweavex/**`
  (27 classes across `crypto`, `determinism`, `graph`, `ir`, `kernel`, `knowledge`,
  `memory`, `persistence`, `query`, `reconstruction`, `replay`), `src/test/java/**`
  (parity + unit suites), `src/test/resources/parity/golden_vectors*.json`, and the
  Java session reports/certifications.
- **`tools/` Java scripts (6)** — `gen_java_parity_matrix.py`,
  `gen_java_parity_vectors{,_s2,_s3}.py`, `generate_parity_manifest.py`,
  `validate_java_manifest.py` (plus this audit's `audit_java_branch.py`). These
  import the **canonical Python `core.*`** package directly (verified) and emit the
  golden vectors + matrix the Java tests assert against — they are the parity bridge,
  not Dart tooling.
- **`.github/workflows/` Java CI (3)** — `java-build.yml`, `java-parity.yml`,
  `parity-regression.yml` (coverage floor 94 %, proven-API floor 17).
- **`PARITY_MANIFEST.json`** — single source of truth for the 128-API surface,
  shared by all four languages; consumed by the Java matrix generator + validator.

## Category 2 — Shared governance (97, all `keep` except README `rewrite`)

Language-neutral: `LICENSE`, `NOTICE`, `AUTHORS`, `CITATION.cff`, `.gitignore`,
`CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `GOVERNANCE.md`, `MAINTAINERS.md`,
`CODEOWNERS`, `SECURITY.md`, `SUPPORT.md`, `ROADMAP.md`, `CHANGELOG.md`, `RELEASE.md`,
the cross-language reference docs (`ARCHITECTURE.md`, `API_REFERENCE.md`,
`AI_AGENT_GUIDE.md`), `.github/` issue/PR templates + `FUNDING.yml`, and the entire
`docs/` reference tree (72 files: architecture spec, cross-language parity model,
ecosystem matrix, security/kaalka/replay references, and the historical `docs/archive`).

`README.md` is the sole `rewrite`: it currently advertises a pub.dev/Dart package
and must become a Maven-Central/Java README (Phase 3).

> **Note on `docs/`:** kept as shared cross-language reference. Some files carry
> Dart-era phrasing (`DART_GAP_AUDIT.md`, `JAVASCRIPT_GAP_AUDIT.md`); they document
> the *shared* contract and per-language gaps, so they are reference material rather
> than Dart build artifacts. `docs/archive/` becomes the destination for relocated
> Dart/JS/Python root checklists.

## Category 3 — Legacy Dart (273)

- **`lib/**` (191)** and **`test/**` (56)** — the Dart library and its test suite.
  These are the substance of the `dart` branch; on the Java branch they are dead
  weight. → `remove`.
- **`example/parity_example.dart`** → `remove`.
- **Root Dart build/config/release (5)** — `pubspec.yaml`, `.pubignore`,
  `analysis_options.yaml`, `PUB_RELEASE_CHECKLIST.md`, `CERTIFICATION.md` (the Dart
  certification narrative). → `relocate` to `docs/archive/`.
- **`.github/workflows/dart.yml`** (Dart CI) → `remove`.
- **Dart files in `validation/` (13) and `cross_language_verifier/` (6)** — `.dart`
  parity/cert harnesses. → `remove`.

## Category 4 — Legacy JavaScript (10)

- **`NPM_RELEASE_CHECKLIST.md`** → `relocate` to `docs/archive/`.
- **`.mjs`/`.js` harnesses** in `cross_language_verifier/` (5) and `validation/` (4)
  → `remove`.

## Category 5 — Legacy Python / multi-language (169)

- **`PYPI_RELEASE_CHECKLIST.md`** → `relocate` to `docs/archive/`.
- **`.github/workflows/ci.yml`** — Python CI (`pip install -e`, `pytest`, wheel
  build) targeting `main`/`master`; no Python package exists on this branch. → `remove`.
- **`tools/` non-Java Python (11)** — `dart_parity_audit.py`, `three_way_parity.py`,
  `generate_reports.py`, `complete_proof_audit.py`, `proof_coverage.py`,
  `cov_breakdown.py`, `gen_api_reference.py`, `gen_executable_matrix.py`,
  `gen_proof_matrix.py`, `gen_semantic_ir_map.py`, `gen_semantic_ir_phaseplan.py`.
  These drive the Dart/multi-language certification, **not** the Java build or Java
  governance (which use only the 6 `gen_java_*`/`validate_java_*` scripts). → `remove`.
- **`validation/` (98) + `cross_language_verifier/` (48) Python + their JSON/MD
  outputs, and the root `*.json` reports (11)** — the multi-language certification
  corpus (`zero_trust_v2`, `release`, `semantic_ir`, parity vectors, inventory and
  audit reports). None is read by the Maven build or `validate_java_manifest.py`.
  → `remove`.

## Key judgment calls

1. **`validation/` + `cross_language_verifier/` are NOT Java parity infrastructure.**
   The Java parity proof is self-contained: `java/src/test/resources/parity/golden_vectors*.json`
   are generated by `tools/gen_java_parity_vectors*.py` from the canonical Python `core`
   and asserted by `CrossLanguageParity*Test`; governance is `validate_java_manifest.py`
   over `PARITY_MANIFEST.json`. Neither tree is imported by any of these. They are the
   Dart/JS/Python multi-language harnesses and are removed.
2. **Python tooling is split, not blanket-kept.** Only the 6 `gen_java_*`/
   `generate_parity_manifest`/`validate_java_manifest` scripts are Java-required;
   the other 11 Python tools are Dart/cert-era and removed.
3. **`docs/` is kept** as shared cross-language reference rather than purged — it is
   documentation, not build/source, and removing it would not make the branch more
   "Maven-native" while it does carry the canonical-spec and architecture material.
4. **Relocate vs remove.** The 7 human-meaningful, single-page Dart/JS/Python root
   config + release-checklist + certification files are *relocated* to `docs/archive/`
   (the mission's named destination); the bulk machine-generated source/test/harness
   trees are *removed* (documented here and in `JAVA_CLEANUP_REPORT.md`; fully
   recoverable from git history and the sibling branches).

## After cleanup (projected)

| Disposition | Files | Net branch shape |
| --- | ---: | --- |
| keep | 170 | `java/` Maven project + Java tooling/CI + shared governance + `docs/` |
| relocate | 7 | under `docs/archive/` |
| remove | 445 | gone from `java` branch (live on `dart`/`python`/`javascript`) |

Projected post-cleanup tracked files: **~177** (170 kept + 7 relocated), down from 623
— a Maven-first branch whose root no longer reads as a pub.dev package.
