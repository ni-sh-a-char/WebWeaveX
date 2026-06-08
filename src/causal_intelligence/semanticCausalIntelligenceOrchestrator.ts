/**
 * Converted from Python: core/causal_intelligence/semantic_causal_intelligence_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildSemanticCausalityGraph } from "./semanticCausalityGraphEngine.js";
import { buildRuntimeFailureLineage } from "./runtimeFailureLineageEngine.js";
import { propagateDistributedState } from "./distributedPropagationEngine.js";
import { analyzeRecoveryCausality } from "./semanticRecoveryCausalityEngine.js";
import { computeRuntimeEquilibrium } from "./runtimeEquilibriumEngine.js";
import { forecastRuntimeInstability } from "./semanticInstabilityForecastEngine.js";
import { analyzeExecutionTiming } from "./executionTimingSemanticsEngine.js";
import { analyzeDependencyCascade } from "./dependencyCascadeIntelligenceEngine.js";
import { buildMutationLineage } from "./semanticRuntimeMutationLineageEngine.js";
import { computeSchedulingPressure } from "./distributedSchedulingPressureEngine.js";
import { analyzeDriftCausality } from "./runtimeDriftCausalityEngine.js";
import { replayCausalSequence } from "./semanticCausalReplayEngine.js";
import { forecastRecoveryOutcome } from "./semanticRecoveryForecastEngine.js";
import { assessSemanticEquilibrium } from "./runtimeSemanticEquilibriumEngine.js";
import { traceExecutionMutations } from "./semanticExecutionMutationEngine.js";
import { propagateRuntimeWaves } from "./semanticRuntimeWavePropagationEngine.js";
import { buildDistributedCausalGraph } from "./distributedRuntimeCausalGraphEngine.js";
import { measureRuntimeResonance } from "./semanticRuntimeResonanceEngine.js";
import { forecastStabilityHorizon } from "./semanticExecutionStabilityHorizonEngine.js";

export function orchestrateSemanticCausalIntelligence(runtime_ir: any): any {
  var causality_graph: any = buildSemanticCausalityGraph(runtime_ir);
  py.setItem(runtime_ir, "runtime_causality_graph", causality_graph);
  var failure_lineage: any = buildRuntimeFailureLineage(runtime_ir);
  var propagation: any = propagateDistributedState(runtime_ir);
  py.setItem(runtime_ir, "distributed_propagation", propagation);
  var recovery: any = analyzeRecoveryCausality(runtime_ir);
  py.setItem(runtime_ir, "recovery_causality", recovery);
  var equilibrium: any = computeRuntimeEquilibrium(runtime_ir);
  py.setItem(runtime_ir, "runtime_equilibrium", equilibrium);
  var instability: any = forecastRuntimeInstability(runtime_ir);
  py.setItem(runtime_ir, "instability_forecast", instability);
  var timing: any = analyzeExecutionTiming(runtime_ir);
  var cascade: any = analyzeDependencyCascade(runtime_ir);
  var mutation_lineage: any = buildMutationLineage(runtime_ir);
  var scheduling_pressure: any = computeSchedulingPressure(runtime_ir);
  var baseline: any = py.pyDict(py.or2(py.get(runtime_ir, "baseline", {}), () => ({})));
  var drift_causality: any = analyzeDriftCausality(runtime_ir, baseline);
  var causal_replay: any = replayCausalSequence(runtime_ir);
  var recovery_forecast: any = forecastRecoveryOutcome(runtime_ir);
  var semantic_equilibrium: any = assessSemanticEquilibrium(runtime_ir);
  var execution_mutations: any = traceExecutionMutations([...py.iter(py.or2(py.get(runtime_ir, "transitions", []), () => ([])))]);
  var waves: any = propagateRuntimeWaves(py.get(propagation, "propagation_paths", []));
  var distributed_causal_graph: any = buildDistributedCausalGraph(runtime_ir);
  var resonance: any = measureRuntimeResonance(runtime_ir);
  var stability_horizon: any = forecastStabilityHorizon(runtime_ir);
  return {"causality_graph": causality_graph, "failure_lineage": failure_lineage, "distributed_propagation": propagation, "recovery_causality": recovery, "runtime_equilibrium": equilibrium, "instability_forecast": instability, "execution_timing": timing, "dependency_cascade": cascade, "mutation_lineage": mutation_lineage, "scheduling_pressure": scheduling_pressure, "drift_causality": drift_causality, "causal_replay": causal_replay, "recovery_forecast": recovery_forecast, "semantic_equilibrium": semantic_equilibrium, "execution_mutations": execution_mutations, "wave_propagation": waves, "distributed_causal_graph": distributed_causal_graph, "runtime_resonance": resonance, "stability_horizon": stability_horizon, "deterministic": true, "bounded": true};
}
export { analyzeDependencyCascade, analyzeDriftCausality, analyzeExecutionTiming, analyzeRecoveryCausality, assessSemanticEquilibrium, buildDistributedCausalGraph, buildMutationLineage, buildRuntimeFailureLineage, buildSemanticCausalityGraph, computeRuntimeEquilibrium, computeSchedulingPressure, forecastRecoveryOutcome, forecastRuntimeInstability, forecastStabilityHorizon, measureRuntimeResonance, propagateDistributedState, propagateRuntimeWaves, replayCausalSequence, traceExecutionMutations };
