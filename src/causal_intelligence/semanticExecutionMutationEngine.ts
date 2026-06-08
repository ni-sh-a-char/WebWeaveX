/**
 * Converted from Python: core/causal_intelligence/semantic_execution_mutation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_MUTATIONS: any = 1000;
export function traceExecutionMutations(transitions: any): any {
  var ordered: any = py.slice(py.sorted(transitions, {key: ((x: any) => [py.toStr(py.get(x, "from")), py.toStr(py.get(x, "to"))]) as (item: any) => any}), null, MAX_MUTATIONS);
  var mutations: any = py.enumerate(ordered).map(([idx, t]: any) => ({"mutation_id": idx, "from": py.get(t, "from"), "to": py.get(t, "to")}));
  return {"mutations": mutations, "mutation_count": py.len(mutations), "bounded": true};
}
