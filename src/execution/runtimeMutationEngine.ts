/**
 * Converted from Python: core/execution/runtime_mutation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function trackRuntimeMutations(prior: any = null, mutation: any = null): any {
  var mutations: any = [...py.iter(py.or2(prior, () => ([])))];
  if (py.truthy(mutation)) {
    var entry: any = {"kind": py.toStr(py.get(mutation, "kind", "unknown")), "target": py.toStr(py.get(mutation, "target", "")), "tick": py.toInt(py.get(mutation, "tick", 0)), "ordered_index": py.len(mutations)};
    py.listAppend(mutations, entry);
  }
  var sorted_mutations: any = py.sorted(mutations, {key: ((item: any) => [py.toInt(py.get(item, "tick", 0)), py.toInt(py.get(item, "ordered_index", 0)), py.toStr(py.get(item, "kind", ""))]) as (item: any) => any});
  var by_kind: any = {"dom": py.iter(sorted_mutations).filter((m: any) => py.eq(py.get(m, "kind"), "dom")).map((m: any) => m), "native": py.iter(sorted_mutations).filter((m: any) => py.eq(py.get(m, "kind"), "native")).map((m: any) => m), "workflow": py.iter(sorted_mutations).filter((m: any) => py.eq(py.get(m, "kind"), "workflow")).map((m: any) => m), "synchronization": py.iter(sorted_mutations).filter((m: any) => py.eq(py.get(m, "kind"), "sync")).map((m: any) => m), "memory": py.iter(sorted_mutations).filter((m: any) => py.eq(py.get(m, "kind"), "memory")).map((m: any) => m)};
  return {"mutations": sorted_mutations, "by_kind": by_kind, "count": py.len(sorted_mutations), "deterministic_order": true, "bounded": true};
}
