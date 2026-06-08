/**
 * Converted from Python: core/memory/runtime_merge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { federateRuntimeMemory } from "./runtimeFederationEngine.js";
import { buildRuntimeMemory } from "./runtimeMemoryEngine.js";

export function mergeRuntimeMemories(memories: any): any {
  var ordered: any = py.sorted(memories, {key: ((m: any) => py.toStr(py.get(m, "memory_id", py.get(m, "runtime_id", "")))) as (item: any) => any});
  var mem: any;
  for (mem of py.iter(ordered)) {
    var history: any = py.get(mem, "runtime_history", []);
    if ((Array.isArray(history))) {
      py.setItem(mem, "runtime_history", py.sorted(history, {key: ((h: any) => [py.toInt(py.get(h, "tick", 0)), py.toStr(py.get(h, "kind", "")), py.toStr(py.get(h, "source", ""))]) as (item: any) => any}));
    }
  }
  var federated: any = federateRuntimeMemory(ordered);
  return buildRuntimeMemory(py.get(federated, "runtime_history", []), py.get(federated, "lineage", []), py.get(federated, "semantic_relations", []));
}
export { buildRuntimeMemory, federateRuntimeMemory };
