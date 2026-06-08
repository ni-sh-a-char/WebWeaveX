/**
 * Converted from Python: core/evolution/semantic_runtime_mutation_planner.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_MUTATIONS: any = 1000;
export function planRuntimeMutation(runtime: any): any {
  return {"mutation_candidates": py.slice(py.sorted(py.keys(runtime)), null, MAX_MUTATIONS), "bounded": true};
}
