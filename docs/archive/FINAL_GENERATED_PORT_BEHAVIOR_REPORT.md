# FINAL GENERATED PORT BEHAVIOR REPORT

**Measured:** 2026-05-29T09:32:45.835330+00:00

## Summary

| Status | Count |
|--------|-------|
| PROTECTED_TESTED | 21 |
| PASS | 0 |
| FAIL | 0 |
| UNTESTED | 1703 |
| `@ts-nocheck` (generated) | 1702 |

## Verdict

**Generated-port behavioral equivalence: NOT PROVEN**

- UNTESTED generated modules: **1703** (certification blocked while > 0)
- Equivalence harness families passing: 20

Protected operational modules are validated via differential vectors and hand-written parity.
AST-generated modules require per-engine probe expansion — topology alone is insufficient.

## Sample (first 50 UNTESTED)

| Python | TypeScript | @ts-nocheck | Exports |
|--------|------------|-------------|---------|| `core/actors/__init__.py` | `src/actors/index.ts` | yes | — |
| `core/actors/semantic_actor_engine.py` | `src/actors/semanticActorEngine.ts` | yes | class:SemanticActor, class:SemanticActorSystem |
| `core/adaptive/__init__.py` | `src/adaptive/index.ts` | yes | — |
| `core/adaptive/adaptive_recovery_engine.py` | `src/adaptive/adaptiveRecoveryEngine.ts` | yes | function:recoverAdaptiveRuntime |
| `core/adaptive/adaptive_runtime_graph_engine.py` | `src/adaptive/adaptiveRuntimeGraphEngine.ts` | yes | function:buildAdaptiveRuntimeGraph |
| `core/adaptive/adaptive_runtime_orchestrator.py` | `src/adaptive/adaptiveRuntimeOrchestrator.ts` | yes | function:runAdaptiveExtraction |
| `core/adaptive/adaptive_snapshot_engine.py` | `src/adaptive/adaptiveSnapshotEngine.ts` | yes | function:buildAdaptiveSnapshot |
| `core/adaptive/dom_similarity_engine.py` | `src/adaptive/domSimilarityEngine.ts` | yes | function:computeDomSimilarity |
| `core/adaptive/extraction_consistency_engine.py` | `src/adaptive/extractionConsistencyEngine.ts` | yes | function:verifyExtractionConsistency |
| `core/adaptive/extraction_fallback_engine.py` | `src/adaptive/extractionFallbackEngine.ts` | yes | function:buildExtractionFallbackChain |
| `core/adaptive/extraction_memory_engine.py` | `src/adaptive/extractionMemoryEngine.ts` | yes | function:rememberExtractionRuntime, function:restoreExtractionRuntime, function:saveAdaptiveMemory, function:loadAdaptiveMemory |
| `core/adaptive/infinite_scroll_recovery_engine.py` | `src/adaptive/infiniteScrollRecoveryEngine.ts` | yes | function:recoverInfiniteScroll |
| `core/adaptive/interaction_recovery_engine.py` | `src/adaptive/interactionRecoveryEngine.ts` | yes | function:recoverInteractionFlow |
| `core/adaptive/layout_resilience_engine.py` | `src/adaptive/layoutResilienceEngine.ts` | yes | function:assessLayoutResilience |
| `core/adaptive/modal_recovery_engine.py` | `src/adaptive/modalRecoveryEngine.ts` | yes | function:recoverModalRuntime |
| `core/adaptive/pagination_recovery_engine.py` | `src/adaptive/paginationRecoveryEngine.ts` | yes | function:recoverPaginationFlow |
| `core/adaptive/replay_alignment_engine.py` | `src/adaptive/replayAlignmentEngine.ts` | yes | function:alignReplayState |
| `core/adaptive/runtime_adaptation_engine.py` | `src/adaptive/runtimeAdaptationEngine.ts` | yes | function:runRuntimeAdaptation |
| `core/adaptive/runtime_reconciliation_engine.py` | `src/adaptive/runtimeReconciliationEngine.ts` | yes | function:reconcileRuntimeState |
| `core/adaptive/runtime_state_alignment_engine.py` | `src/adaptive/runtimeStateAlignmentEngine.ts` | yes | function:alignRuntimeState |
| `core/adaptive/schema_stability_engine.py` | `src/adaptive/schemaStabilityEngine.ts` | yes | function:stabilizeExtractionSchema |
| `core/adaptive/selector_healing_engine.py` | `src/adaptive/selectorHealingEngine.ts` | yes | function:healSelector |
| `core/adaptive/semantic_anchor_engine.py` | `src/adaptive/semanticAnchorEngine.ts` | yes | function:buildSemanticAnchor |
| `core/agents/__init__.py` | `src/agents/index.ts` | yes | — |
| `core/agents/agent_reasoning_engine.py` | `src/agents/agentReasoningEngine.ts` | yes | function:summarizeForAgent |
| `core/agents/chunk_query_engine.py` | `src/agents/chunkQueryEngine.ts` | yes | function:queryChunks |
| `core/agents/document_query_engine.py` | `src/agents/documentQueryEngine.ts` | yes | function:queryDocument |
| `core/agents/extraction_query_engine.py` | `src/agents/extractionQueryEngine.ts` | yes | function:queryExtraction |
| `core/agents/graph_query_engine.py` | `src/agents/graphQueryEngine.ts` | yes | function:queryNodes, function:queryEdges, function:queryDependencies, function:queryServices |
| `core/agents/graph_query_language.py` | `src/agents/graphQueryLanguage.ts` | yes | function:runGql |
| `core/agents/repository_query_engine.py` | `src/agents/repositoryQueryEngine.ts` | yes | function:queryRepository |
| `core/agents/semantic_agent_engine.py` | `src/agents/semanticAgentEngine.ts` | yes | class:SemanticAgent |
| `core/agents/semantic_agent_runtime.py` | `src/agents/semanticAgentRuntime.ts` | yes | class:SemanticAgentRuntime |
| `core/agents/semantic_capability_router.py` | `src/agents/semanticCapabilityRouter.ts` | yes | function:routeSemanticCapability |
| `core/agents/semantic_task_graph_engine.py` | `src/agents/semanticTaskGraphEngine.ts` | yes | function:buildSemanticTaskGraph |
| `core/agents/traversal_query_engine.py` | `src/agents/traversalQueryEngine.ts` | yes | function:tracePaths |
| `core/application/__init__.py` | `src/application/index.ts` | yes | — |
| `core/application/action_graph_engine.py` | `src/application/actionGraphEngine.ts` | yes | function:buildActionGraph |
| `core/application/application_checkpoint_engine.py` | `src/application/applicationCheckpointEngine.ts` | yes | function:saveApplicationCheckpoint, function:loadApplicationCheckpoint |
| `core/application/application_cognition_orchestrator.py` | `src/application/applicationCognitionOrchestrator.ts` | yes | function:runApplicationCognition |
| `core/application/application_context_engine.py` | `src/application/applicationContextEngine.ts` | yes | function:buildApplicationContext |
| `core/application/application_intent_engine.py` | `src/application/applicationIntentEngine.ts` | yes | function:resolveApplicationIntent |
| `core/application/application_memory_engine.py` | `src/application/applicationMemoryEngine.ts` | yes | function:rememberApplicationRuntime, function:restoreApplicationRuntime, function:saveApplicationMemory, function:loadApplicationMemory |
| `core/application/application_recovery_engine.py` | `src/application/applicationRecoveryEngine.ts` | yes | function:recoverApplicationRuntime |
| `core/application/application_replay_engine.py` | `src/application/applicationReplayEngine.ts` | yes | function:replayApplicationRuntime |
| `core/application/application_runtime_alignment_engine.py` | `src/application/applicationRuntimeAlignmentEngine.ts` | yes | function:alignApplicationRuntime |
| `core/application/application_session_graph_engine.py` | `src/application/applicationSessionGraphEngine.ts` | yes | function:buildApplicationSessionGraph |
| `core/application/application_state_engine.py` | `src/application/applicationStateEngine.ts` | yes | function:buildApplicationState |
| `core/application/application_topology_engine.py` | `src/application/applicationTopologyEngine.ts` | yes | function:buildApplicationTopology |
| `core/application/application_transition_engine.py` | `src/application/applicationTransitionEngine.ts` | yes | function:buildApplicationTransitions |

```json
{
  "measured_at": "2026-05-29T09:32:45.835330+00:00",
  "counts": {
    "PASS": 0,
    "FAIL": 0,
    "UNTESTED": 1703,
    "PROTECTED_TESTED": 21
  },
  "untested_generated": 1703,
  "nocheck_generated": 1702,
  "execution_equivalence_proven": false,
  "certification_blocked": true
}
```
