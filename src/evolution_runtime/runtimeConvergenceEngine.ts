/**
 * Converted from Python: core/evolution_runtime/runtime_convergence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function convergeRuntimeEvolution(evolutions: any): any {
  var merged_mutations: any[] = [];
  var seen: Set<any> = new Set();
  var evolution: any;
  for (evolution of py.iter(py.sorted(evolutions, {key: ((item: any) => py.toStr(py.get(item, "evolution_id", ""))) as (item: any) => any}))) {
    var mutation: any;
    for (mutation of py.iter(py.get(evolution, "mutations", []))) {
      var key: any = [py.get(mutation, "kind"), py.toStr(py.get(mutation, "target"))];
      if (py.contains(seen, key)) {
        continue;
      }
      py.setAdd(seen, key);
      py.listAppend(merged_mutations, mutation);
    }
  }
  return {"converged_mutations": py.sorted(merged_mutations, {key: ((item: any) => [py.get(item, "kind", ""), py.toStr(py.get(item, "target", ""))]) as (item: any) => any}), "evolution_count": py.len(evolutions), "consistent": true, "bounded": true};
}
