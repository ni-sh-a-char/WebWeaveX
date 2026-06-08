/**
 * Converted from Python: core/causal_intelligence/semantic_recovery_forecast_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function forecastRecoveryOutcome(runtime_ir: any): any {
  var recovery: any = py.get(runtime_ir, "recovery_causality", {});
  if (!((recovery !== null && typeof recovery === "object" && !Array.isArray(recovery) && !(recovery instanceof Set) && !(recovery instanceof Map)))) {
    recovery = analyzeRecoveryInline(runtime_ir);
  }
  var possible: any = py.get(recovery, "recovery_possible", false);
  return {"recovery_forecast": (py.truthy(possible) ? "successful" : "unavailable"), "deterministic": true};
}
export function analyzeRecoveryInline(runtime_ir: any): any {
  var journal: any = py.get(runtime_ir, "journal", {});
  var entries: any = (((journal !== null && typeof journal === "object" && !Array.isArray(journal) && !(journal instanceof Set) && !(journal instanceof Map))) ? py.get(journal, "entries", []) : []);
  return {"recovery_possible": py.truthy(entries)};
}
