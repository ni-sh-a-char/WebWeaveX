/**
 * Converted from Python: core/evolution_runtime/runtime_mutation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_MUTATIONS: any = 10000;
export function buildRuntimeMutations(selector: any, workflow: any, semantic: any, sync: any): any {
  var mutations: any[] = [];
  var item: any;
  for (item of py.iter(py.slice(py.get(selector, "selectors", []), null, MAX_MUTATIONS))) {
    py.listAppend(mutations, {"kind": "selector", "target": py.toStr(py.get(item, "original", "")), "evolved": py.toStr(py.get(item, "evolved", ""))});
  }
  if (py.truthy(py.get(workflow, "execution_ordering"))) {
    py.listAppend(mutations, {"kind": "workflow", "target": "execution_ordering", "evolved": py.at(workflow, "execution_ordering")});
  }
  if (py.truthy(py.get(semantic, "domain"))) {
    py.listAppend(mutations, {"kind": "semantic", "target": "domain", "evolved": py.at(semantic, "domain")});
  }
  if (py.truthy(py.get(sync, "convergence"))) {
    py.listAppend(mutations, {"kind": "sync", "target": "convergence", "evolved": true});
  }
  return py.sorted(mutations, {key: ((item: any) => [py.at(item, "kind"), py.toStr(py.at(item, "target"))]) as (item: any) => any});
}
