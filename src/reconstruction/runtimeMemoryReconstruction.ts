/**
 * Converted from Python: core/reconstruction/runtime_memory_reconstruction.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reconstructRuntimeMemory(memory_ir: any = null, semantic: any = null, lineage: any = null): any {
  memory_ir = py.or2(memory_ir, () => ({}));
  semantic = py.or2(semantic, () => ({}));
  lineage = py.or2(lineage, () => ({}));
  var runtime_history: any = py.get(memory_ir, "runtime_history", {});
  if (((runtime_history !== null && typeof runtime_history === "object" && !Array.isArray(runtime_history) && !(runtime_history instanceof Set) && !(runtime_history instanceof Map)))) {
    var history_list: any = py.get(runtime_history, "runtime_history", []);
  } else {
    history_list = ((Array.isArray(runtime_history)) ? runtime_history : []);
  }
  var lineage_body: any = py.or2(lineage, () => (py.get(memory_ir, "lineage", {})));
  var lineage_entries: any = (((lineage_body !== null && typeof lineage_body === "object" && !Array.isArray(lineage_body) && !(lineage_body instanceof Set) && !(lineage_body instanceof Map))) ? py.get(lineage_body, "lineage", lineage_body) : lineage_body);
  return {"semantic_memory": py.pyDict(py.or2(semantic, () => (py.get(memory_ir, "semantic", {})))), "lineage": py.sorted(((Array.isArray(lineage_entries)) ? lineage_entries : []), {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "continuity": py.pyDict(py.get(memory_ir, "knowledge", {})), "runtime_graph_memory": py.pyDict(py.get(memory_ir, "memory_graphs", {})), "synchronization_history": py.iter(history_list).filter((item: any) => py.eq(py.get(item, "kind"), "sync")).map((item: any) => item), "bounded": true};
}
