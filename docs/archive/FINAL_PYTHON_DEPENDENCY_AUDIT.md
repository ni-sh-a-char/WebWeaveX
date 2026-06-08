# FINAL PYTHON DEPENDENCY AUDIT

**Measured:** 2026-06-08T08:49:55.996118+00:00

## Summary

| Classification | Hits |
|----------------|------|
| REMOVE | 236 |
| REPLACE | 1019 |
| SAFE | 15216 |
| SAFE (Node-native subprocess — non-Python target) | 6 |
| SAFE (dev script — not runtime) | 28 |
| SAFE (dev tooling) | 402 |
| SAFE (language identifier / URL corpus) | 484 |
| SAFE (provenance comment) | 1705 |

| npm `package.json` dev scripts invoking Python | 31 |
| `src/` runtime REPLACE hits | 0 |

## Verdict

**`src/` has no subprocess/Python runtime invocations.**

**Validation layer still invokes Python for differential/real-world gates — REPLACE (Phase 4).**

## REMOVE (runtime coupling)

- `GOVERNANCE.md:7` [python] — `- **Python** (`origin/python`) is the canonical runtime and specification source.`
- `package.json:79` [python] — `"convergence:vectors": "python tools/runtime_vectors/generate_canonical_vectors.py",`
- `README.md:407` [python] — `JavaScript implements **bounded operational Tier D** ports aligned with Python (`origin/python`):`
- `README.md:496` [python] — `WebWeaveX maintains a **bounded semantic fabric**: ontology classes, lineage, reconciliation, and graph cognition. Protected modules (`src/semantic/*`, `src/wor`
- `README.md:532` [python,pip] — `Convergence is **specification-anchored**: `specification/` is the sole authority; both the `origin/python` (pip) and `javascript` (npm) products conform to it `
- `.github/workflows/nightly.yml:20` [python] — `- run: python tools/runtime_vectors/generate_canonical_vectors.py`
- `docs/architecture/FINAL_TOTAL_PARITY_AUDIT.md:4` [python] — `**Branches audited:** `origin/python` · `origin/javascript` · `origin/dart` · `origin/main``
- `docs/archive/FINAL_CROSS_LANGUAGE_EQUALITY_REPORT.md:4` [python,pip] — `**Authority:** `specification/` (sole). Both `origin/python` (pip) and the `javascript` (npm) products conform to it; neither is canonical.`
- `docs/archive/FINAL_DECOUPLING_REPORT.md:17` [python] — `| `validation/differential/common.ts` | REPLACE | Load vectors from specification/vectors; drop origin/python authority |`
- `docs/archive/FINAL_FORENSIC_EQUALITY_REPORT.md:9` [python] — `| Asset | Python (origin/python) | JavaScript (src/) |`
- `docs/archive/FINAL_FORENSIC_SUBSYSTEM_AUDIT.md:7` [python] — `| Python `core/` modules (origin/python) | 1724 |`
- `docs/archive/FINAL_INDEPENDENT_CERTIFICATION.md:18` [python] — `> The Python fix lives on local branch `python-cert-fix` (worktree off `origin/python`). It is **not yet committed/pushed to `origin/python`** — until merged th`
- `docs/archive/FINAL_INDEPENDENT_CERTIFICATION.md:26` [python] — `**Python (`python-cert-fix` off `origin/python`):** import-chain fix, clean-venv build+install, full import-symbol audit, public-API certification, **full pytes`
- `docs/archive/FINAL_INDEPENDENT_CERTIFICATION.md:77` [python] — `- **The Python fix is not yet on `origin/python`** — verified on `python-cert-fix` only.`
- `docs/archive/FINAL_INDEPENDENT_CERTIFICATION.md:136` [python,pip] — `- **Python independent product:** YES (on `python-cert-fix`). pip-installable in a clean venv outside the repo, Node-free, imports cleanly, 772 tests pass, publ`
- `docs/archive/FINAL_INDEPENDENT_CERTIFICATION.md:140` [python] — `**Honest bottom line:** both halves of the vision are achieved and independently certified from fresh execution evidence on Windows. The single remaining action`
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:31` [python] — `- `validation/differential/common.ts:61` — `if (data.source === "origin/python") {``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:32` [python] — `- `validation/forensic/subsystemAudit.ts:32` — `const pyCore = gitCount("origin/python", "core/", ".py");``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:33` [python] — `- `validation/forensic/subsystemAudit.ts:56` — ``| Python \`core/\` modules (origin/python) | ${pyCore} |`,``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:34` [python] — `- `validation/vectors/browser_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:35` [python] — `- `validation/vectors/continuation_memory_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:36` [python] — `- `validation/vectors/continuation_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:37` [python] — `- `validation/vectors/distributed_memory_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:38` [python] — `- `validation/vectors/distributed_replay_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:39` [python] — `- `validation/vectors/distributed_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:40` [python] — `- `validation/vectors/graph_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:41` [python] — `- `validation/vectors/memory_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:42` [python] — `- `validation/vectors/ontology_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:43` [python] — `- `validation/vectors/orchestration_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:44` [python] — `- `validation/vectors/parser_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:45` [python] — `- `validation/vectors/reconstruction_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:46` [python] — `- `validation/vectors/replay_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:47` [python] — `- `validation/vectors/repository_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:48` [python] — `- `validation/vectors/runtime_identity_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:49` [python] — `- `validation/vectors/runtime_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:50` [python] — `- `validation/vectors/semantic_reconciliation_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:51` [python] — `- `validation/vectors/semantic_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:52` [python] — `- `validation/vectors/vm_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:53` [python] — `- `validation/vectors/workflow_graph_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:54` [python] — `- `validation/vectors/workflow_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:55` [python] — `- `tests/generated/vectorConformance.test.ts:27` — `expect(["webweavex-spec", "origin/python"]).toContain(data.source);``
- `docs/archive/FINAL_OSS_CERTIFICATION.md:7` [python] — `| Python workflows (origin/python) | 1 |`
- `docs/archive/FINAL_PUBLIC_API_CERTIFICATION.md:7` [python] — `Evidence: Python `__all__` from `origin/python:webweavex/__init__.py`; JavaScript surface = runtime `Object.keys()` of the built `dist/index.js`.`
- `docs/archive/FINAL_PYTHON_CERTIFICATION.md:9` [python,pip] — `The **pip install webweavex** product is built from the `origin/python` branch / PyPI package, not this JavaScript monorepo.`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:29` [python] — `- `GOVERNANCE.md:7` [python] — `- **Python** (`origin/python`) is the canonical runtime and specification source.``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:30` [python] — `- `package.json:79` [python] — `"convergence:vectors": "python tools/runtime_vectors/generate_canonical_vectors.py",``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:31` [python] — `- `README.md:407` [python] — `JavaScript implements **bounded operational Tier D** ports aligned with Python (`origin/python`):``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:33` [python,pip] — `- `README.md:532` [python,pip] — `Convergence is **specification-anchored**: `specification/` is the sole authority; both the `origin/python` (pip) and `javascr`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:34` [python] — `- `.github/workflows/nightly.yml:20` [python] — `- run: python tools/runtime_vectors/generate_canonical_vectors.py``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:35` [python] — `- `docs/architecture/FINAL_TOTAL_PARITY_AUDIT.md:4` [python] — `**Branches audited:** `origin/python` · `origin/javascript` · `origin/dart` · `origin/main```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:36` [python,pip] — `- `docs/archive/FINAL_CROSS_LANGUAGE_EQUALITY_REPORT.md:4` [python,pip] — `**Authority:** `specification/` (sole). Both `origin/python` (pip) and the `javascrip`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:37` [python] — `- `docs/archive/FINAL_DECOUPLING_REPORT.md:17` [python] — `| `validation/differential/common.ts` | REPLACE | Load vectors from specification/vectors; drop origi`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:38` [python] — `- `docs/archive/FINAL_FORENSIC_EQUALITY_REPORT.md:9` [python] — `| Asset | Python (origin/python) | JavaScript (src/) |``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:39` [python] — `- `docs/archive/FINAL_FORENSIC_SUBSYSTEM_AUDIT.md:7` [python] — `| Python `core/` modules (origin/python) | 1724 |``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:40` [python,pip] — `- `docs/archive/FINAL_INDEPENDENT_CERTIFICATION.md:14` [python,pip] — `| **Python (pip), as-is on `origin/python`** | **FAIL — package does not import** | measu`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:41` [python,pip] — `- `docs/archive/FINAL_INDEPENDENT_CERTIFICATION.md:17` [python,pip] — `**The original vision is ACHIEVED for the JavaScript product and NOT YET ACHIEVED for the`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:42` [python] — `- `docs/archive/FINAL_INDEPENDENT_CERTIFICATION.md:28` [python] — `**Python product (`origin/python`, materialized read-only):** clean-venv wheel install, packa`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:43` [python,subprocess] — `- `docs/archive/FINAL_INDEPENDENT_CERTIFICATION.md:54` [python,subprocess] — `| RULE 3 (Python Node-free) | **0** subprocess/import of node/npm/npx/tsx in `orig`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:44` [python] — `- `docs/archive/FINAL_INDEPENDENT_CERTIFICATION.md:68` [python] — `- The Python product import-fix was applied and verified **only in a local materialized copy*`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:45` [python] — `- `docs/archive/FINAL_INDEPENDENT_CERTIFICATION.md:124` [python] — `git archive origin/python | tar -x -C _pyproduct``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:48` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:31` [python] — `- `validation/differential/common.ts:61` — `if (data.source === "origin/python") {```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:49` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:32` [python] — `- `validation/forensic/subsystemAudit.ts:32` — `const pyCore = gitCount("origin/python", "core/", `
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:50` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:33` [python] — `- `validation/forensic/subsystemAudit.ts:56` — ``| Python \`core/\` modules (origin/python) | ${py`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:51` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:34` [python] — `- `validation/vectors/browser_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:52` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:35` [python] — `- `validation/vectors/continuation_memory_vectors/canonical.json:4` — `"source": "origin/python",``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:53` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:36` [python] — `- `validation/vectors/continuation_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:54` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:37` [python] — `- `validation/vectors/distributed_memory_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:55` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:38` [python] — `- `validation/vectors/distributed_replay_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:56` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:39` [python] — `- `validation/vectors/distributed_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:57` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:40` [python] — `- `validation/vectors/graph_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:58` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:41` [python] — `- `validation/vectors/memory_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:59` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:42` [python] — `- `validation/vectors/ontology_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:60` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:43` [python] — `- `validation/vectors/orchestration_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:61` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:44` [python] — `- `validation/vectors/parser_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:62` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:45` [python] — `- `validation/vectors/reconstruction_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:63` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:46` [python] — `- `validation/vectors/replay_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:64` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:47` [python] — `- `validation/vectors/repository_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:65` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:48` [python] — `- `validation/vectors/runtime_identity_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:66` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:49` [python] — `- `validation/vectors/runtime_vectors/canonical.json:4` — `"source": "origin/python",```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:67` [python] — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:50` [python] — `- `validation/vectors/semantic_reconciliation_vectors/canonical.json:4` — `"source": "origin/pytho`
- _…and 156 more_

## REPLACE (migrate to specification authority)

- `SECURITY.md:15` — `- Production execution forbids `eval`, `exec`, and arbitrary subprocess invocation`
- `docs/architecture/DART_GAP_AUDIT.md:15` — `| **NFKC normalization** | ⚠️ | Node.js subprocess when on PATH |`
- `docs/archive/FINAL_DECOUPLING_REPORT.md:16` — `| `validation/real_world/validateRealWorld.ts` | REPLACE | Remove execSync python; use JS-only URL corpus probes |`
- `docs/archive/FINAL_DECOUPLING_REPORT.md:27` — `- `src/` has **0** subprocess/Python runtime invocations (see FINAL_PYTHON_DEPENDENCY_AUDIT.md)`
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:13` — `| Python subprocess in `validation/` (publish path) | **0** |`
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:57` — `## SUPPORT (subprocess in `src/`, non-Python target — RULE 2 compliant)`
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:59` — `- `src/browser/syncPlaywright.ts:8` [child_process] — `import { spawnSync } from "node:child_process";``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:60` — `- `src/runtime/pyCompat.ts:30` [child_process] — `import * as childProcessModule from "node:child_process";``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:61` — `- `src/runtime/pyCompat.ts:2863` [child_process] — `let _cp: typeof import("node:child_process") | null = null;``
- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:62` — `- `src/runtime/pyCompat.ts:2865` [child_process] — `function requireChildProcess(): typeof import("node:child_process") {``
- `docs/archive/FINAL_JS_PORT_REPORT.md:4` — `- Zero Python subprocess or PyPI dependency`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:12` — `| SAFE (Node-native subprocess — non-Python target) | 6 |`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:23` — `**`src/` has no subprocess/Python runtime invocations.**`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:113` — `- `SECURITY.md:15` — `- Production execution forbids `eval`, `exec`, and arbitrary subprocess invocation``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:114` — `- `docs/architecture/DART_GAP_AUDIT.md:15` — `| **NFKC normalization** | ⚠️ | Node.js subprocess when on PATH |``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:115` — `- `docs/archive/FINAL_DECOUPLING_REPORT.md:16` — `| `validation/real_world/validateRealWorld.ts` | REPLACE | Remove execSync python; use JS-only URL corpus prob`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:116` — `- `docs/archive/FINAL_DECOUPLING_REPORT.md:27` — `- `src/` has **0** subprocess/Python runtime invocations (see FINAL_PYTHON_DEPENDENCY_AUDIT.md)``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:117` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:13` — `| Python subprocess in `validation/` (publish path) | **0** |``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:118` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:57` — `## SUPPORT (subprocess in `src/`, non-Python target — RULE 2 compliant)``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:119` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:59` — `- `src/browser/syncPlaywright.ts:8` [child_process] — `import { spawnSync } from "node:child_process";```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:120` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:60` — `- `src/runtime/pyCompat.ts:30` [child_process] — `import * as childProcessModule from "node:child_process";`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:121` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:61` — `- `src/runtime/pyCompat.ts:2863` [child_process] — `let _cp: typeof import("node:child_process") | null = n`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:122` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:62` — `- `src/runtime/pyCompat.ts:2865` [child_process] — `function requireChildProcess(): typeof import("node:chi`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:123` — `- `docs/archive/FINAL_JS_PORT_REPORT.md:4` — `- Zero Python subprocess or PyPI dependency``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:124` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:12` — `| SAFE (Node-native subprocess — non-Python target) | 6 |``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:125` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:23` — `**`src/` has no subprocess/Python runtime invocations.**``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:126` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:113` — `- `SECURITY.md:15` — `- Production execution forbids `eval`, `exec`, and arbitrary subprocess invocatio`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:127` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:114` — `- `docs/architecture/DART_GAP_AUDIT.md:15` — `| **NFKC normalization** | ⚠️ | Node.js subprocess when o`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:128` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:115` — `- `docs/archive/FINAL_DECOUPLING_REPORT.md:16` — `| `validation/real_world/validateRealWorld.ts` | REPL`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:129` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:116` — `- `docs/archive/FINAL_DECOUPLING_REPORT.md:27` — `- `src/` has **0** subprocess/Python runtime invocati`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:130` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:117` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:13` — `| Python subprocess in `validation/` (publish path`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:131` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:118` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:57` — `## SUPPORT (subprocess in `src/`, non-Python targe`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:132` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:119` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:59` — `- `src/browser/syncPlaywright.ts:8` [child_process`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:133` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:120` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:60` — `- `src/runtime/pyCompat.ts:30` [child_process] — ``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:134` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:121` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:61` — `- `src/runtime/pyCompat.ts:2863` [child_process] —`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:135` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:122` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:62` — `- `src/runtime/pyCompat.ts:2865` [child_process] —`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:136` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:123` — `- `docs/archive/FINAL_JS_PORT_REPORT.md:4` — `- Zero Python subprocess or PyPI dependency```
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:137` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:124` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:112` — `- `SECURITY.md:15` — `- Production execution f`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:138` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:125` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:113` — `- `docs/architecture/DART_GAP_AUDIT.md:15` — ``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:140` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:127` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:115` — `- `docs/archive/FINAL_DECOUPLING_REPORT.md:27``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:141` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:128` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:116` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:142` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:129` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:117` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:143` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:130` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:118` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:144` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:131` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:119` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:145` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:132` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:120` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:146` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:133` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:121` — `- `docs/archive/FINAL_JS_DECOUPLING_REPORT.md:`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:147` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:134` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:122` — `- `docs/archive/FINAL_JS_PORT_REPORT.md:4` — ``
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:175` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:178` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:166` — `- `src/browser/syncPlaywright.ts:4` — `* once `
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:176` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:179` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:167` — `- `src/browser/syncPlaywright.ts:8` — `import `
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:177` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:180` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:168` — `- `src/browser/syncPlaywright.ts:108` — `/* v8`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:178` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:181` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:169` — `- `src/runtime/pyCompat.ts:30` — `import * as `
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:179` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:182` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:170` — `- `src/runtime/pyCompat.ts:2863` — `let _cp: t`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:180` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:183` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:171` — `- `src/runtime/pyCompat.ts:2865` — `function r`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:182` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:185` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:181` — `- `tests/protected/handPorts.test.ts:2` — `imp`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:183` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:186` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:190` — `- `validation/generateFinalReports.ts:1` — `im`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:184` — `- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:187` — `- `docs/archive/FINAL_SELF_CONTAINED_NPM_CERTIFICATION.md:9` — `| src/ runtime free of python subproces`
- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md:185` — `- `docs/archive/FINAL_SELF_CONTAINED_NPM_CERTIFICATION.md:9` — `| src/ runtime free of python subprocess | PASS | hits=0 |``
- `docs/archive/FINAL_SELF_CONTAINED_NPM_CERTIFICATION.md:9` — `| src/ runtime free of python subprocess | PASS | hits=0 |`
- `tests/api/publicApiEquality.test.ts:3` — `* specification-equivalent name for every public name in the Python`
- `tests/api/publicApiEquality.test.ts:53` — `describe("RULE 15 — public API equality (Python __all__ ⇄ JS exports)", () => {`
- `tests/api/publicApiEquality.test.ts:56` — `it("exposes every Python public API name", () => {`
- `tests/branches/coverage90Push.test.ts:118` — `registerParser("py", { lang: "python" });`
- `tests/branches/coverage90Push.test.ts:119` — `expect(getParser("py")?.lang).toBe("python");`
- `tests/branches/trueEqualityCoverage.test.ts:150` — `).toEqual(["cargo", "go", "npm", "python"]);`
- `tests/distributed/pythonParityBranches.test.ts:12` — `describe("python parity branches", () => {`
- `tests/protected/branchGaps.test.ts:120` — `describe("python analyzer branch edges", () => {`
- `tests/protected/branchGaps2.test.ts:2` — `import { spawn, type ChildProcess } from "node:child_process";`
- `tests/protected/branchGaps2.test.ts:139` — `server = spawn("python", ["-B", "tools/convergence/probe_http_server.py"], { stdio: "ignore" });`
- `tests/protected/branchGaps3.test.ts:64` — `expect(errOut.parse_error).toContain("<python>");`
- `tests/protected/branchGaps4.test.ts:140` — `const errPy = ParserRegistry.parse("<not python>", "broken.py");`
- `tests/protected/handPorts.test.ts:2` — `import { spawn, type ChildProcess } from "node:child_process";`
- `tests/protected/handPorts.test.ts:44` — `describe("python source analyzer (ast/pythonAstEngine)", () => {`
- `tests/protected/handPorts.test.ts:69` — `it("raises SyntaxError on clearly invalid python", () => {`
- `tests/protected/handPorts.test.ts:83` — `describe("repository python ast summary", () => {`
- `tests/protected/handPorts.test.ts:105` — `it("detects python plus regex-derived symbols", () => {`
- `tests/protected/handPorts.test.ts:160` — `it("matches python json formatting and sorts deeply", () => {`
- `tests/protected/handPorts.test.ts:193` — `it("parses python source end to end", () => {`
- `tests/protected/handPorts.test.ts:219` — `server = spawn("python", ["-B", "tools/convergence/probe_http_server.py"], {`
- `tests/protected/handPorts.test.ts:229` — `it("provides the python sync_api object graph", () => {`
- `validation/generateFinalReports.ts:1` — `import { execSync } from "node:child_process";`
- _…and 939 more_

## SAFE (dev tooling sample)

- `CHANGELOG.md:11` — `- Cross-language parity with Python via `kaalka@5.0.0` + canonical normalization pipeline`
- `CHANGELOG.md:26` — `- **Repository AST cognition** — Python AST + multi-language structural parsers`
- `CONTRIBUTING.md:10` — `pip install -e ".[dev,browser]"`
- `CONTRIBUTING.md:18` — `python -m build`
- `CONTRIBUTING.md:19` — `python -c "import webweavex; assert webweavex.__version__ == '2.0.0'"`
- `FINAL_TRUE_PARITY_REPORT.md:4` — `**Canonical reference:** `python` branch (production runtime — unchanged)`
- `FINAL_TRUE_PARITY_REPORT.md:11` — `WebWeaveX now exposes **operational subsystem parity** across Python, JavaScript, and Dart:`
- `FINAL_TRUE_PARITY_REPORT.md:13` — `| Capability | Python | JavaScript | Dart |`
- `FINAL_TRUE_PARITY_REPORT.md:25` — `**Python** retains full multi-engine production depth (connectors, distributed extraction, semantic `
- `FINAL_TRUE_PARITY_REPORT.md:52` — `# Python`
- `FINAL_TRUE_PARITY_REPORT.md:53` — `PYTHONPATH=. python validation/validate_ecosystem.py`
- `FINAL_TRUE_PARITY_REPORT.md:71` — `| Connector fleet | Python-only production connectors |`
- `FINAL_TRUE_PARITY_REPORT.md:72` — `| Semantic VM / distributed | Python-only production orchestration |`
- `FINAL_TRUE_PARITY_REPORT.md:80` — `WebWeaveX is **deterministic runtime cognition infrastructure for humans and AI agents** — equal ope`
- `GOVERNANCE.md:8` — `- **JavaScript** (`javascript`) converges to Python via forensic audits and differential validation.`
- `MAINTAINERS.md:7` — `- Preserve Python as canonical source of truth`
- `MAINTAINERS.md:9` — `- Review changes to `core/` (Python), `src/` (JavaScript), validators, and specs under `docs/specs/``
- `package-lock.json:1744` — `"license": "Python-2.0"`
- `package.json:73` — `"convert:python": "python tools/py2ts/py2ts.py",`
- `package.json:74` — `"convergence:audit": "python tools/convergence/forensic_equality_audit.py",`
- `package.json:75` — `"convergence:true-equality-audit": "python -B tools/convergence/true_equality_audit.py",`
- `package.json:76` — `"convergence:port": "python tools/convergence/port_all.py",`
- `package.json:77` — `"convergence:specs": "python tools/specgen/generate_all_specs.py",`
- `package.json:78` — `"convergence:validators": "python tools/convergence/generate_validators.py",`
- `package.json:80` — `"convergence:verify-ports": "python tools/convergence/verify_generated_ports.py",`
- `package.json:81` — `"convergence:coverage-probe": "python tools/convergence/coverage_probe.py",`
- `package.json:82` — `"convergence:semantic-repair": "python tools/convergence/semantic_repair.py",`
- `package.json:83` — `"convergence:generate-tests": "python tools/convergence/generate_vector_tests.py",`
- `package.json:86` — `"convergence:verify-port-behavior": "python -B tools/convergence/verify_generated_port_behavior.py",`
- `package.json:87` — `"certification:omega": "python -B tools/convergence/omega_certification.py",`