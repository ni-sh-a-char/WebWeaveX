# PRE-COMMIT CHANGE INVENTORY

**Measured:** 2026-06-08T07:30:32.267938+00:00

Total entries: 883 (52 modified, 831 untracked).

## Classification

| Class | Count | Disposition |
|-------|-------|-------------|
| Intentional (modified, tracked) | 52 | commit |
| Intentional/generated (untracked) | 831 | commit |
| Accidental / contamination | 0 | EXCLUDED (gitignored) |
| Unknown | 0 | — |

## Accidental (excluded via .gitignore)


## Untracked-to-commit by area

| Area | Count |
|------|-------|
| generated/protected TS (py2ts + hand-written) | 404 |
| certification reports + committable evidence (docs/archive *.md, docs/specs *.json matrices) | 375 |
| equivalence/differential harnesses + buildRuntimeGraph migrations | 21 |
| new + migrated test suites | 18 |
| CI workflows | 6 |
| governance / release docs | 5 |
| specification/vectors authority | 1 |
| new certification generators (build_public_api.py, certify_public_api.py) | 1 |

## Modified tracked files (all intentional)

- `.gitignore`
- `README.md`
- `docs/archive/FINAL_CROSS_LANGUAGE_EQUALITY_REPORT.md`
- `docs/archive/FINAL_JS_RELEASE_REPORT.md`
- `docs/archive/FINAL_NPM_READINESS_REPORT.md`
- `docs/archive/FINAL_PARITY_REPORT.md`
- `docs/archive/FINAL_README_AUDIT.md`
- `docs/archive/FINAL_REAL_WORLD_VALIDATION_REPORT.md`
- `docs/archive/FINAL_REPOSITORY_STRUCTURE_REPORT.md`
- `docs/archive/FINAL_TRUE_EQUALITY_REPORT.md`
- `package-lock.json`
- `package.json`
- `src/browser/authenticatedRuntime.ts`
- `src/connectors/index.ts`
- `src/connectors/liveRuntimeOrchestrator.ts`
- `src/contracts/graphContracts.ts`
- `src/contracts/runtimeContracts.ts`
- `src/crypto/kaalkaRuntime.ts`
- `src/determinism/globalRuntimeFingerprint.ts`
- `src/distributed/distributedAdaptiveRuntimeEngine.ts`
- `src/distributed/distributedExtractionOrchestrator.ts`
- `src/distributed/distributedIdentityEngine.ts`
- `src/distributed/distributedMonitoringEngine.ts`
- `src/distributed/distributedRecoveryEngine.ts`
- `src/distributed/distributedStreamEngine.ts`
- `src/distributed/runtimeFederationEngine.ts`
- `src/graph/runtimeGraph.ts`
- `src/graph/runtimeGraphReconstruction.ts`
- `src/index.ts`
- `src/kernel/runtimePipeline.ts`
- `src/memory/runtimeMemoryGraph.ts`
- `src/orchestration/extractionPlanner.ts`
- `src/orchestration/extractionScheduler.ts`
- `src/orchestration/extractionStateEngine.ts`
- `src/orchestration/extractionStrategyEngine.ts`
- `src/orchestration/orchestrationEngine.ts`
- `src/replay/replayEquivalence.ts`
- `src/semantic/semanticJournal.ts`
- `tests/integration/fullStack.test.ts`
- `tests/replay/replayDom.test.ts`
- `validation/generateFinalReports.ts`
- `validation/orchestration/validateOrchestration.ts`
- `validation/parity/js_vectors.json`
- `validation/parity/parity_report.md`
- `validation/reconstruction/validateReconstruction.ts`
- `validation/replay/replay_report.md`
- `validation/replay/replay_vectors.json`
- `validation/replay/validateReplay.ts`
- `validation/runtime_graph/validateRuntimeGraph.ts`
- `validation/runtime_memory/validateRuntimeMemory.ts`
- `validation/validateEcosystem.ts`
- `vitest.config.ts`

_LF→CRLF warnings on Windows are benign line-ending normalisation; git normalises on add._
