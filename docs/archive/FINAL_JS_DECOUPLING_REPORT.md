# FINAL JS DECOUPLING REPORT

**Measured:** 2026-06-07T19:05:37.267886+00:00

**Status:** PASS (runtime surface)

## Targets

| Target | Value |
|--------|-------|
| Python Runtime Dependency in `src/` | **0** |
| Python Execution Dependency in `src/` | **0** |
| Python subprocess in `validation/` (publish path) | **0** |

## Classification summary

| Class | Count |
|-------|-------|
| BLOCKER | 2 |
| REPLACE | 25 |
| SAFE | 2158 |
| SUPPORT | 4 |

## BLOCKER (must fix before npm consumer runs Python)

- `tests/protected/branchGaps2.test.ts:139` [python_invoke] — `server = spawn("python", ["-B", "tools/convergence/probe_http_server.py"], { stdio: "ignore" });`
- `tests/protected/handPorts.test.ts:219` [python_invoke] — `server = spawn("python", ["-B", "tools/convergence/probe_http_server.py"], {`

## REPLACE (rename / spec-native)

- `validation/differential/common.ts:61` — `if (data.source === "origin/python") {`
- `validation/forensic/subsystemAudit.ts:32` — `const pyCore = gitCount("origin/python", "core/", ".py");`
- `validation/forensic/subsystemAudit.ts:56` — ``| Python \`core/\` modules (origin/python) | ${pyCore} |`,`
- `validation/vectors/browser_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/continuation_memory_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/continuation_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/distributed_memory_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/distributed_replay_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/distributed_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/graph_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/memory_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/ontology_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/orchestration_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/parser_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/reconstruction_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/replay_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/repository_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/runtime_identity_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/runtime_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/semantic_reconciliation_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/semantic_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/vm_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/workflow_graph_vectors/canonical.json:4` — `"source": "origin/python",`
- `validation/vectors/workflow_vectors/canonical.json:4` — `"source": "origin/python",`
- `tests/generated/vectorConformance.test.ts:27` — `expect(["webweavex-spec", "origin/python"]).toContain(data.source);`

## SUPPORT (subprocess in `src/`, non-Python target — RULE 2 compliant)

- `src/browser/syncPlaywright.ts:8` [child_process] — `import { spawnSync } from "node:child_process";`
- `src/runtime/pyCompat.ts:30` [child_process] — `import * as childProcessModule from "node:child_process";`
- `src/runtime/pyCompat.ts:2863` [child_process] — `let _cp: typeof import("node:child_process") | null = null;`
- `src/runtime/pyCompat.ts:2865` [child_process] — `function requireChildProcess(): typeof import("node:child_process") {`

_Verified spawn targets in `src/`: `curl` (HTTP shim) and `process.execPath`/`node` (Playwright bridge). No `python`/`pyodide` target anywhere in the runtime surface._

## Verified

- Published `files` field: `dist`, `README.md`, `LICENSE` only
- Dev-only Python: `package.json` scripts (22), `tools/*` — not in npm tarball

**Python Validation Dependency:** non-zero in dev `validation/` — default gates are JS-only (`validate:differential`, `validate:equivalence`).
