/**
 * Converted from Python: core/kernel/runtime_registry.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _PHASES: any = ["browser", "semantic", "workflow", "synchronization", "evolution", "connectors", "memory", "execution", "reconstruction"];
export function registerRuntimePhase(registry: any, phase: any, payload: any): any {
  var phases: any = py.pyDict(py.get(registry, "phases", {}));
  py.setItem(phases, phase, payload);
  return {"phases": phases, "registered": py.sorted(py.keys(phases)), "bounded": true};
}
export function listRuntimePhases(): any {
  return [...py.iter(_PHASES)];
}
