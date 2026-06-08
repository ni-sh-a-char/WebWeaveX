# FINAL GENERATED CODE AUDIT

**Measured:** 2026-05-29T12:51:42.986123+00:00

## Summary

| Metric | Value |
|--------|-------|
| Python `core/*.py` modules | 1724 |
| Generated TS (non-protected) | 1707 |
| `@ts-nocheck` in generated | 0 |
| Protected operational modules | 138 |
| Sample audited (first 500 py paths) | 500 |

## Verdict

**Generated module behavioral validation: NOT COMPLETE**

Topology mirrors exist for most modules; per-module execution probes are not automated at scale.
Protected modules are hand-authored overrides and require differential vectors + targeted tests.

## Sample module registry

| Python | TypeScript | Exists | Protected | @ts-nocheck | Exports (sample) |
|--------|------------|--------|-----------|-------------|------------------|| `core/__init__.py` | `src/index.ts` | yes | yes | no | const:VERSION || `core/actors/__init__.py` | `src/actors/index.ts` | yes | no | no | — || `core/actors/semantic_actor_engine.py` | `src/actors/semanticActorEngine.ts` | yes | no | no | class:SemanticActor, class:SemanticActorSystem || `core/adaptive/__init__.py` | `src/adaptive/index.ts` | yes | no | no | — || `core/adaptive/adaptive_recovery_engine.py` | `src/adaptive/adaptiveRecoveryEngine.ts` | yes | no | no | function:recoverAdaptiveRuntime || `core/adaptive/adaptive_runtime_graph_engine.py` | `src/adaptive/adaptiveRuntimeGraphEngine.ts` | yes | no | no | function:buildAdaptiveRuntimeGraph || `core/adaptive/adaptive_runtime_orchestrator.py` | `src/adaptive/adaptiveRuntimeOrchestrator.ts` | yes | no | no | function:runAdaptiveExtraction || `core/adaptive/adaptive_snapshot_engine.py` | `src/adaptive/adaptiveSnapshotEngine.ts` | yes | no | no | function:buildAdaptiveSnapshot || `core/adaptive/dom_similarity_engine.py` | `src/adaptive/domSimilarityEngine.ts` | yes | no | no | function:computeDomSimilarity || `core/adaptive/extraction_consistency_engine.py` | `src/adaptive/extractionConsistencyEngine.ts` | yes | no | no | function:verifyExtractionConsistency || `core/adaptive/extraction_fallback_engine.py` | `src/adaptive/extractionFallbackEngine.ts` | yes | no | no | function:buildExtractionFallbackChain || `core/adaptive/extraction_memory_engine.py` | `src/adaptive/extractionMemoryEngine.ts` | yes | no | no | function:rememberExtractionRuntime, function:restoreExtractionRuntime, function:saveAdaptiveMemory, function:loadAdaptiveMemory || `core/adaptive/infinite_scroll_recovery_engine.py` | `src/adaptive/infiniteScrollRecoveryEngine.ts` | yes | no | no | function:recoverInfiniteScroll || `core/adaptive/interaction_recovery_engine.py` | `src/adaptive/interactionRecoveryEngine.ts` | yes | no | no | function:recoverInteractionFlow || `core/adaptive/layout_resilience_engine.py` | `src/adaptive/layoutResilienceEngine.ts` | yes | no | no | function:assessLayoutResilience || `core/adaptive/modal_recovery_engine.py` | `src/adaptive/modalRecoveryEngine.ts` | yes | no | no | function:recoverModalRuntime || `core/adaptive/pagination_recovery_engine.py` | `src/adaptive/paginationRecoveryEngine.ts` | yes | no | no | function:recoverPaginationFlow || `core/adaptive/replay_alignment_engine.py` | `src/adaptive/replayAlignmentEngine.ts` | yes | no | no | function:alignReplayState || `core/adaptive/runtime_adaptation_engine.py` | `src/adaptive/runtimeAdaptationEngine.ts` | yes | no | no | function:runRuntimeAdaptation || `core/adaptive/runtime_reconciliation_engine.py` | `src/adaptive/runtimeReconciliationEngine.ts` | yes | no | no | function:reconcileRuntimeState || `core/adaptive/runtime_state_alignment_engine.py` | `src/adaptive/runtimeStateAlignmentEngine.ts` | yes | no | no | function:alignRuntimeState || `core/adaptive/schema_stability_engine.py` | `src/adaptive/schemaStabilityEngine.ts` | yes | no | no | function:stabilizeExtractionSchema || `core/adaptive/selector_healing_engine.py` | `src/adaptive/selectorHealingEngine.ts` | yes | no | no | function:healSelector || `core/adaptive/semantic_anchor_engine.py` | `src/adaptive/semanticAnchorEngine.ts` | yes | no | no | function:buildSemanticAnchor || `core/agents/__init__.py` | `src/agents/index.ts` | yes | no | no | — || `core/agents/agent_reasoning_engine.py` | `src/agents/agentReasoningEngine.ts` | yes | no | no | function:summarizeForAgent || `core/agents/chunk_query_engine.py` | `src/agents/chunkQueryEngine.ts` | yes | no | no | function:queryChunks || `core/agents/document_query_engine.py` | `src/agents/documentQueryEngine.ts` | yes | no | no | function:queryDocument || `core/agents/extraction_query_engine.py` | `src/agents/extractionQueryEngine.ts` | yes | no | no | function:queryExtraction || `core/agents/graph_query_engine.py` | `src/agents/graphQueryEngine.ts` | yes | no | no | function:queryNodes, function:queryEdges, function:queryDependencies, function:queryServices || `core/agents/graph_query_language.py` | `src/agents/graphQueryLanguage.ts` | yes | no | no | function:runGql || `core/agents/repository_query_engine.py` | `src/agents/repositoryQueryEngine.ts` | yes | no | no | function:queryRepository || `core/agents/semantic_agent_engine.py` | `src/agents/semanticAgentEngine.ts` | yes | no | no | class:SemanticAgent || `core/agents/semantic_agent_runtime.py` | `src/agents/semanticAgentRuntime.ts` | yes | no | no | class:SemanticAgentRuntime || `core/agents/semantic_capability_router.py` | `src/agents/semanticCapabilityRouter.ts` | yes | no | no | function:routeSemanticCapability || `core/agents/semantic_task_graph_engine.py` | `src/agents/semanticTaskGraphEngine.ts` | yes | no | no | function:buildSemanticTaskGraph || `core/agents/traversal_query_engine.py` | `src/agents/traversalQueryEngine.ts` | yes | no | no | function:tracePaths || `core/application/__init__.py` | `src/application/index.ts` | yes | no | no | — || `core/application/action_graph_engine.py` | `src/application/actionGraphEngine.ts` | yes | no | no | function:buildActionGraph || `core/application/application_checkpoint_engine.py` | `src/application/applicationCheckpointEngine.ts` | yes | no | no | function:saveApplicationCheckpoint, function:loadApplicationCheckpoint || `core/application/application_cognition_orchestrator.py` | `src/application/applicationCognitionOrchestrator.ts` | yes | no | no | function:runApplicationCognition || `core/application/application_context_engine.py` | `src/application/applicationContextEngine.ts` | yes | no | no | function:buildApplicationContext || `core/application/application_intent_engine.py` | `src/application/applicationIntentEngine.ts` | yes | no | no | function:resolveApplicationIntent || `core/application/application_memory_engine.py` | `src/application/applicationMemoryEngine.ts` | yes | no | no | function:rememberApplicationRuntime, function:restoreApplicationRuntime, function:saveApplicationMemory, function:loadApplicationMemory || `core/application/application_recovery_engine.py` | `src/application/applicationRecoveryEngine.ts` | yes | no | no | function:recoverApplicationRuntime || `core/application/application_replay_engine.py` | `src/application/applicationReplayEngine.ts` | yes | no | no | function:replayApplicationRuntime || `core/application/application_runtime_alignment_engine.py` | `src/application/applicationRuntimeAlignmentEngine.ts` | yes | no | no | function:alignApplicationRuntime || `core/application/application_session_graph_engine.py` | `src/application/applicationSessionGraphEngine.ts` | yes | no | no | function:buildApplicationSessionGraph || `core/application/application_state_engine.py` | `src/application/applicationStateEngine.ts` | yes | no | no | function:buildApplicationState || `core/application/application_topology_engine.py` | `src/application/applicationTopologyEngine.ts` | yes | no | no | function:buildApplicationTopology || `core/application/application_transition_engine.py` | `src/application/applicationTransitionEngine.ts` | yes | no | no | function:buildApplicationTransitions || `core/application/dashboard_runtime_engine.py` | `src/application/dashboardRuntimeEngine.ts` | yes | no | no | function:buildDashboardRuntime || `core/application/form_runtime_engine.py` | `src/application/formRuntimeEngine.ts` | yes | no | no | function:buildFormRuntime || `core/application/navigation_semantic_engine.py` | `src/application/navigationSemanticEngine.ts` | yes | no | no | function:buildNavigationSemantics || `core/application/objective_execution_engine.py` | `src/application/objectiveExecutionEngine.ts` | yes | no | no | function:executeRuntimeObjective || `core/application/runtime_goal_engine.py` | `src/application/runtimeGoalEngine.ts` | yes | no | no | function:buildRuntimeGoal || `core/application/ui_semantic_engine.py` | `src/application/uiSemanticEngine.ts` | yes | no | no | function:extractUiSemantics || `core/application/workflow_graph_engine.py` | `src/application/workflowGraphEngine.ts` | yes | no | no | function:buildWorkflowGraph || `core/archive/__init__.py` | `src/archive/index.ts` | yes | no | no | — || `core/archive/archive_extraction_engine.py` | `src/archive/archiveExtractionEngine.ts` | yes | no | no | function:extractArchive || `core/ast/__init__.py` | `src/ast/index.ts` | yes | no | no | — || `core/ast/control_flow_engine.py` | `src/ast/controlFlowEngine.ts` | yes | no | no | function:buildControlFlowGraph || `core/ast/execution_path_engine.py` | `src/ast/executionPathEngine.ts` | yes | no | no | function:reconstructExecutionPaths || `core/ast/python_ast_engine.py` | `src/ast/pythonAstEngine.ts` | yes | no | no | function:parsePythonAst || `core/ast/semantic_ast_ir_engine.py` | `src/ast/semanticAstIrEngine.ts` | yes | no | no | function:compileSemanticAstIr || `core/ast/symbol_resolution_engine.py` | `src/ast/symbolResolutionEngine.ts` | yes | no | no | function:resolveSymbols || `core/auth/__init__.py` | `src/auth/index.ts` | yes | no | no | — || `core/auth/authentication_runtime_engine.py` | `src/auth/authenticationRuntimeEngine.ts` | yes | no | no | function:authenticateRuntime, function:rotateAuthenticatedSession || `core/auth/cookie_runtime_engine.py` | `src/auth/cookieRuntimeEngine.ts` | yes | no | no | function:extractCookies, function:injectCookies || `core/auth/csrf_runtime_engine.py` | `src/auth/csrfRuntimeEngine.ts` | yes | no | no | function:extractCsrfTokens || `core/auth/session_restoration_engine.py` | `src/auth/sessionRestorationEngine.ts` | yes | no | no | function:restoreAuthenticatedSession || `core/auth/token_runtime_engine.py` | `src/auth/tokenRuntimeEngine.ts` | yes | no | no | function:extractAuthTokens, function:injectAuthTokens || `core/autonomy/__init__.py` | `src/autonomy/index.ts` | yes | no | no | — || `core/autonomy/semantic_autonomous_orchestrator.py` | `src/autonomy/semanticAutonomousOrchestrator.ts` | yes | no | no | function:orchestrateSemanticRuntime || `core/autonomy/semantic_cognitive_state_engine.py` | `src/autonomy/semanticCognitiveStateEngine.ts` | yes | no | no | function:buildSemanticCognitiveState || `core/autonomy/semantic_constraint_solver.py` | `src/autonomy/semanticConstraintSolver.ts` | yes | no | no | function:solveSemanticConstraints || `core/autonomy/semantic_dependency_scheduler.py` | `src/autonomy/semanticDependencyScheduler.ts` | yes | no | no | function:scheduleSemanticDependencies || `core/autonomy/semantic_execution_heuristics_engine.py` | `src/autonomy/semanticExecutionHeuristicsEngine.ts` | yes | no | no | function:computeExecutionHeuristics || `core/autonomy/semantic_goal_engine.py` | `src/autonomy/semanticGoalEngine.ts` | yes | no | no | function:resolveSemanticGoal || `core/autonomy/semantic_intent_resolution_engine.py` | `src/autonomy/semanticIntentResolutionEngine.ts` | yes | no | no | function:resolveSemanticIntent || `core/autonomy/semantic_knowledge_synthesis_engine.py` | `src/autonomy/semanticKnowledgeSynthesisEngine.ts` | yes | no | no | function:synthesizeSemanticKnowledge || `core/autonomy/semantic_learning_memory_engine.py` | `src/autonomy/semanticLearningMemoryEngine.ts` | yes | no | no | class:SemanticLearningMemory || `core/autonomy/semantic_multi_agent_coordination_engine.py` | `src/autonomy/semanticMultiAgentCoordinationEngine.ts` | yes | no | no | function:coordinateSemanticAgents || `core/autonomy/semantic_planning_engine.py` | `src/autonomy/semanticPlanningEngine.ts` | yes | no | no | function:planSemanticAutonomy || `core/autonomy/semantic_predictive_execution_engine.py` | `src/autonomy/semanticPredictiveExecutionEngine.ts` | yes | no | no | function:predictSemanticExecution || `core/autonomy/semantic_reflex_engine.py` | `src/autonomy/semanticReflexEngine.ts` | yes | no | no | function:triggerSemanticReflex || `core/autonomy/semantic_resource_forecast_engine.py` | `src/autonomy/semanticResourceForecastEngine.ts` | yes | no | no | function:forecastSemanticResources || `core/autonomy/semantic_runtime_arbitration_engine.py` | `src/autonomy/semanticRuntimeArbitrationEngine.ts` | yes | no | no | function:arbitrateSemanticRuntime || `core/autonomy/semantic_runtime_health_engine.py` | `src/autonomy/semanticRuntimeHealthEngine.ts` | yes | no | no | function:assessRuntimeHealth || `core/autonomy/semantic_runtime_recovery_engine.py` | `src/autonomy/semanticRuntimeRecoveryEngine.ts` | yes | no | no | function:recoverSemanticRuntime || `core/autonomy/semantic_safety_envelope_engine.py` | `src/autonomy/semanticSafetyEnvelopeEngine.ts` | yes | no | no | function:enforceSemanticSafetyEnvelope || `core/autonomy/semantic_semanticity_validator.py` | `src/autonomy/semanticSemanticityValidator.ts` | yes | no | no | function:validateSemanticity || `core/autonomy/semantic_task_decomposition_engine.py` | `src/autonomy/semanticTaskDecompositionEngine.ts` | yes | no | no | function:decomposeSemanticTask || `core/browser/__init__.py` | `src/browser/index.ts` | yes | no | no | — || `core/browser/dom_stabilization_engine.py` | `src/browser/domStabilizationEngine.ts` | yes | no | no | function:stabilizeDomHtml, function:computeStableDomHash, function:stabilizeExtractionPayload, function:stableBrowserIrFingerprint || `core/browser/html_semantic_extraction_engine.py` | `src/browser/htmlSemanticExtractionEngine.ts` | yes | no | no | function:extractSemanticHtml || `core/browser/playwright_runtime.py` | `src/browser/playwrightRuntime.ts` | yes | no | no | function:launchAuthenticatedBrowser, function:restoreAuthenticatedContext, function:persistAuthenticatedContext, function:renderPage || `core/browser/spa_runtime_stabilizer.py` | `src/browser/spaRuntimeStabilizer.ts` | yes | no | no | function:detectSpaFramework, function:stabilizeRoute, function:buildSpaStabilization, function:applySpaStabilizationToRuntime || `core/browser/universal_web_extraction_engine.py` | `src/browser/universalWebExtractionEngine.ts` | yes | no | no | function:extractWeb, class:_InteractivePage || `core/bytecode/__init__.py` | `src/bytecode/index.ts` | yes | no | no | — |

```json
{
  "sample": [
    {
      "python_source": "core/__init__.py",
      "ts_target": "src/index.ts",
      "exists": true,
      "protected": true,
      "ts_nocheck": false,
      "exported_symbols": [
        "const:VERSION"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/actors/__init__.py",
      "ts_target": "src/actors/index.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/actors/semantic_actor_engine.py",
      "ts_target": "src/actors/semanticActorEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "class:SemanticActor",
        "class:SemanticActorSystem"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/__init__.py",
      "ts_target": "src/adaptive/index.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/adaptive_recovery_engine.py",
      "ts_target": "src/adaptive/adaptiveRecoveryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:recoverAdaptiveRuntime"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/adaptive_runtime_graph_engine.py",
      "ts_target": "src/adaptive/adaptiveRuntimeGraphEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:buildAdaptiveRuntimeGraph"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/adaptive_runtime_orchestrator.py",
      "ts_target": "src/adaptive/adaptiveRuntimeOrchestrator.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:runAdaptiveExtraction"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/adaptive_snapshot_engine.py",
      "ts_target": "src/adaptive/adaptiveSnapshotEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:buildAdaptiveSnapshot"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/dom_similarity_engine.py",
      "ts_target": "src/adaptive/domSimilarityEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:computeDomSimilarity"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/extraction_consistency_engine.py",
      "ts_target": "src/adaptive/extractionConsistencyEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:verifyExtractionConsistency"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/extraction_fallback_engine.py",
      "ts_target": "src/adaptive/extractionFallbackEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:buildExtractionFallbackChain"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/extraction_memory_engine.py",
      "ts_target": "src/adaptive/extractionMemoryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:rememberExtractionRuntime",
        "function:restoreExtractionRuntime",
        "function:saveAdaptiveMemory",
        "function:loadAdaptiveMemory"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/infinite_scroll_recovery_engine.py",
      "ts_target": "src/adaptive/infiniteScrollRecoveryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:recoverInfiniteScroll"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/interaction_recovery_engine.py",
      "ts_target": "src/adaptive/interactionRecoveryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:recoverInteractionFlow"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/layout_resilience_engine.py",
      "ts_target": "src/adaptive/layoutResilienceEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:assessLayoutResilience"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/modal_recovery_engine.py",
      "ts_target": "src/adaptive/modalRecoveryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:recoverModalRuntime"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/pagination_recovery_engine.py",
      "ts_target": "src/adaptive/paginationRecoveryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:recoverPaginationFlow"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/replay_alignment_engine.py",
      "ts_target": "src/adaptive/replayAlignmentEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:alignReplayState"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/runtime_adaptation_engine.py",
      "ts_target": "src/adaptive/runtimeAdaptationEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:runRuntimeAdaptation"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/runtime_reconciliation_engine.py",
      "ts_target": "src/adaptive/runtimeReconciliationEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:reconcileRuntimeState"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/runtime_state_alignment_engine.py",
      "ts_target": "src/adaptive/runtimeStateAlignmentEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:alignRuntimeState"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/schema_stability_engine.py",
      "ts_target": "src/adaptive/schemaStabilityEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:stabilizeExtractionSchema"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/selector_healing_engine.py",
      "ts_target": "src/adaptive/selectorHealingEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:healSelector"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/adaptive/semantic_anchor_engine.py",
      "ts_target": "src/adaptive/semanticAnchorEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:buildSemanticAnchor"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/__init__.py",
      "ts_target": "src/agents/index.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/agent_reasoning_engine.py",
      "ts_target": "src/agents/agentReasoningEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:summarizeForAgent"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/chunk_query_engine.py",
      "ts_target": "src/agents/chunkQueryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:queryChunks"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/document_query_engine.py",
      "ts_target": "src/agents/documentQueryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:queryDocument"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/extraction_query_engine.py",
      "ts_target": "src/agents/extractionQueryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:queryExtraction"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/graph_query_engine.py",
      "ts_target": "src/agents/graphQueryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:queryNodes",
        "function:queryEdges",
        "function:queryDependencies",
        "function:queryServices"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/graph_query_language.py",
      "ts_target": "src/agents/graphQueryLanguage.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:runGql"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/repository_query_engine.py",
      "ts_target": "src/agents/repositoryQueryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:queryRepository"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/semantic_agent_engine.py",
      "ts_target": "src/agents/semanticAgentEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "class:SemanticAgent"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/semantic_agent_runtime.py",
      "ts_target": "src/agents/semanticAgentRuntime.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "class:SemanticAgentRuntime"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/semantic_capability_router.py",
      "ts_target": "src/agents/semanticCapabilityRouter.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:routeSemanticCapability"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/semantic_task_graph_engine.py",
      "ts_target": "src/agents/semanticTaskGraphEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:buildSemanticTaskGraph"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/agents/traversal_query_engine.py",
      "ts_target": "src/agents/traversalQueryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:tracePaths"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/__init__.py",
      "ts_target": "src/application/index.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/action_graph_engine.py",
      "ts_target": "src/application/actionGraphEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:buildActionGraph"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/application_checkpoint_engine.py",
      "ts_target": "src/application/applicationCheckpointEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:saveApplicationCheckpoint",
        "function:loadApplicationCheckpoint"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/application_cognition_orchestrator.py",
      "ts_target": "src/application/applicationCognitionOrchestrator.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:runApplicationCognition"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/application_context_engine.py",
      "ts_target": "src/application/applicationContextEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:buildApplicationContext"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/application_intent_engine.py",
      "ts_target": "src/application/applicationIntentEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:resolveApplicationIntent"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/application_memory_engine.py",
      "ts_target": "src/application/applicationMemoryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:rememberApplicationRuntime",
        "function:restoreApplicationRuntime",
        "function:saveApplicationMemory",
        "function:loadApplicationMemory"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/application_recovery_engine.py",
      "ts_target": "src/application/applicationRecoveryEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:recoverApplicationRuntime"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/application_replay_engine.py",
      "ts_target": "src/application/applicationReplayEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:replayApplicationRuntime"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/application_runtime_alignment_engine.py",
      "ts_target": "src/application/applicationRuntimeAlignmentEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:alignApplicationRuntime"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/application_session_graph_engine.py",
      "ts_target": "src/application/applicationSessionGraphEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:buildApplicationSessionGraph"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/application_state_engine.py",
      "ts_target": "src/application/applicationStateEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:buildApplicationState"
      ],
      "behavioral_probe": "NOT RUN"
    },
    {
      "python_source": "core/application/application_topology_engine.py",
      "ts_target": "src/application/applicationTopologyEngine.ts",
      "exists": true,
      "protected": false,
      "ts_nocheck": false,
      "exported_symbols": [
        "function:buildApplicationTopology"
      ],
      "behavioral_probe": "NOT RUN"
    }
  ],
  "nocheck": {
    "generated_total": 1707,
    "nocheck_generated": 0,
    "protected_total": 138
  }
}
```
