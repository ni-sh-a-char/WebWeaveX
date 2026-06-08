/**
 * Converted from Python: core/causal_intelligence/semantic_runtime_mutation_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_MUTATIONS: any = 1000;
export function buildMutationLineage(runtime_ir: any): any {
  var keys: any = py.slice(py.sorted(py.keys(runtime_ir)), null, MAX_MUTATIONS);
  var lineage: any = py.enumerate(keys).map(([idx, key]: any) => ({"step": idx, "key": key, "causal_action": "observe"}));
  return {"mutation_lineage": lineage, "bounded": true};
}
