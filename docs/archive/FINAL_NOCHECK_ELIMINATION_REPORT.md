# FINAL NOCHECK ELIMINATION REPORT

**Measured:** 2026-05-29T10:16:00.413702+00:00

**@ts-nocheck count:** 1702
**Target:** 0

**Status: FAIL** — mass removal without per-file type repair is not applied.

Procedure: fix types/imports/contracts per file, run `npm run typecheck`, then remove directive.

```json
{
  "count": 1702,
  "sample": [
    {
      "path": "src/cacheEngine.ts",
      "protected": false,
      "lines": 145
    },
    {
      "path": "src/executionGraph.ts",
      "protected": false,
      "lines": 27
    },
    {
      "path": "src/extractionEngine.ts",
      "protected": false,
      "lines": 103
    },
    {
      "path": "src/fetchEngine.ts",
      "protected": false,
      "lines": 128
    },
    {
      "path": "src/fullPipeline.ts",
      "protected": false,
      "lines": 99
    },
    {
      "path": "src/graphCompressionEngine.ts",
      "protected": false,
      "lines": 15
    },
    {
      "path": "src/graphExportEngine.ts",
      "protected": false,
      "lines": 16
    },
    {
      "path": "src/graphLineageEngine.ts",
      "protected": false,
      "lines": 15
    },
    {
      "path": "src/graphMergeEngine.ts",
      "protected": false,
      "lines": 32
    },
    {
      "path": "src/graphPartitionEngine.ts",
      "protected": false,
      "lines": 20
    },
    {
      "path": "src/intentEngine.ts",
      "protected": false,
      "lines": 75
    },
    {
      "path": "src/outputEngine.ts",
      "protected": false,
      "lines": 146
    },
    {
      "path": "src/queryBuilder.ts",
      "protected": false,
      "lines": 103
    },
    {
      "path": "src/rankingEngine.ts",
      "protected": false,
      "lines": 169
    },
    {
      "path": "src/sourceOrchestrator.ts",
      "protected": false,
      "lines": 59
    },
    {
      "path": "src/version.ts",
      "protected": false,
      "lines": 14
    },
    {
      "path": "src/actors/index.ts",
      "protected": false,
      "lines": 5
    },
    {
      "path": "src/actors/semanticActorEngine.ts",
      "protected": false,
      "lines": 51
    },
    {
      "path": "src/adaptive/adaptiveRecoveryEngine.ts",
      "protected": false,
      "lines": 19
    },
    {
      "path": "src/adaptive/adaptiveRuntimeGraphEngine.ts",
      "protected": false,
      "lines": 27
    },
    {
      "path": "src/adaptive/adaptiveRuntimeOrchestrator.ts",
      "protected": false,
      "lines": 31
    },
    {
      "path": "src/adaptive/adaptiveSnapshotEngine.ts",
      "protected": false,
      "lines": 16
    },
    {
      "path": "src/adaptive/domSimilarityEngine.ts",
      "protected": false,
      "lines": 28
    },
    {
      "path": "src/adaptive/extractionConsistencyEngine.ts",
      "protected": false,
      "lines": 18
    },
    {
      "path": "src/adaptive/extractionFallbackEngine.ts",
      "protected": false,
      "lines": 21
    },
    {
      "path": "src/adaptive/extractionMemoryEngine.ts",
      "protected": false,
      "lines": 48
    },
    {
      "path": "src/adaptive/index.ts",
      "protected": false,
      "lines": 15
    },
    {
      "path": "src/adaptive/infiniteScrollRecoveryEngine.ts",
      "protected": false,
      "lines": 36
    },
    {
      "path": "src/adaptive/interactionRecoveryEngine.ts",
      "protected": false,
      "lines": 23
    },
    {
      "path": "src/adaptive/layoutResilienceEngine.ts",
      "protected": false,
      "lines": 18
    },
    {
      "path": "src/adaptive/modalRecoveryEngine.ts",
      "protected": false,
      "lines": 47
    },
    {
      "path": "src/adaptive/paginationRecoveryEngine.ts",
      "protected": false,
      "lines": 34
    },
    {
      "path": "src/adaptive/replayAlignmentEngine.ts",
      "protected": false,
      "lines": 21
    },
    {
      "path": "src/adaptive/runtimeAdaptationEngine.ts",
      "protected": false,
      "lines": 24
    },
    {
      "path": "src/adaptive/runtimeReconciliationEngine.ts",
      "protected": false,
      "lines": 16
    },
    {
      "path": "src/adaptive/runtimeStateAlignmentEngine.ts",
      "protected": false,
      "lines": 18
    },
    {
      "path": "src/adaptive/schemaStabilityEngine.ts",
      "protected": false,
      "lines": 37
    },
    {
      "path": "src/adaptive/selectorHealingEngine.ts",
      "protected": false,
      "lines": 72
    },
    {
      "path": "src/adaptive/semanticAnchorEngine.ts",
      "protected": false,
      "lines": 45
    },
    {
      "path": "src/agents/agentReasoningEngine.ts",
      "protected": false,
      "lines": 16
    },
    {
      "path": "src/agents/chunkQueryEngine.ts",
      "protected": false,
      "lines": 15
    },
    {
      "path": "src/agents/documentQueryEngine.ts",
      "protected": false,
      "lines": 16
    },
    {
      "path": "src/agents/extractionQueryEngine.ts",
      "protected": false,
      "lines": 15
    },
    {
      "path": "src/agents/graphQueryEngine.ts",
      "protected": false,
      "lines": 32
    },
    {
      "path": "src/agents/graphQueryLanguage.ts",
      "protected": false,
      "lines": 22
    },
    {
      "path": "src/agents/index.ts",
      "protected": false,
      "lines": 5
    },
    {
      "path": "src/agents/repositoryQueryEngine.ts",
      "protected": false,
      "lines": 16
    },
    {
      "path": "src/agents/semanticAgentEngine.ts",
      "protected": false,
      "lines": 24
    },
    {
      "path": "src/agents/semanticAgentRuntime.ts",
      "protected": false,
      "lines": 25
    },
    {
      "path": "src/agents/semanticCapabilityRouter.ts",
      "protected": false,
      "lines": 22
    }
  ]
}
```
