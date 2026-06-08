/**
 * Converted from Python: core/memory/runtime_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function queryRuntimeMemory(memory: any, query_type: any = "semantic", term: any = ""): any {
  var results: any[] = [];
  if (py.eq(query_type, "semantic")) {
    var relation: any;
    for (relation of py.iter(py.get(memory, "semantic_relations", []))) {
      if ((py.contains(py.toStr(py.get(relation, "from", "")), term) || py.contains(py.toStr(py.get(relation, "to", "")), term))) {
        py.listAppend(results, relation);
      }
    }
  } else if (py.eq(query_type, "lineage")) {
    var item: any;
    for (item of py.iter(py.get(memory, "lineage", []))) {
      if (py.contains(py.toStr(py.get(item, "id", "")), term)) {
        py.listAppend(results, item);
      }
    }
  } else if (py.eq(query_type, "topology")) {
    for (item of py.iter(py.get(memory, "runtime_history", []))) {
      if (py.contains(py.toStr(py.get(item, "runtime", "")), term)) {
        py.listAppend(results, item);
      }
    }
  } else if (py.eq(query_type, "sync")) {
    for (item of py.iter(py.get(memory, "synchronization_history", []))) {
      py.listAppend(results, item);
    }
  } else {
    for (item of py.iter(py.get(memory, "runtime_history", []))) {
      if (py.contains(py.toStr(item), term)) {
        py.listAppend(results, item);
      }
    }
  }
  return {"query_type": query_type, "term": term, "results": py.sorted(results, {key: ((item: any) => py.toStr(item)) as (item: any) => any}), "count": py.len(results), "bounded": true};
}
