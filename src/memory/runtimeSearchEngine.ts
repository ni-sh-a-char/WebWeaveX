/**
 * Converted from Python: core/memory/runtime_search_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function searchRuntimeMemory(index: any, term: any, search_type: any = "structural"): any {
  var matches: any[] = [];
  var normalized: any = py.strip(String(term).toLowerCase());
  if (py.eq(search_type, "semantic")) {
    var key: any;
    var value: any;
    for ([key, value] of py.items(py.get(index, "entity_index", {}))) {
      if (py.contains(String(key).toLowerCase(), normalized)) {
        py.listAppend(matches, {"match": key, "value": value, "kind": "entity"});
      }
    }
  } else if (py.eq(search_type, "lineage")) {
    for ([key, value] of py.items(py.get(index, "workflow_index", {}))) {
      if (py.contains(String(key).toLowerCase(), normalized)) {
        py.listAppend(matches, {"match": key, "value": value, "kind": "workflow"});
      }
    }
  } else if (py.eq(search_type, "graph")) {
    for ([key, value] of py.items(py.get(index, "graph_index", {}))) {
      py.listAppend(matches, {"match": key, "value": value, "kind": "graph"});
    }
  } else {
    var bucket: any;
    for (bucket of py.iter(["entity_index", "workflow_index", "connector_index"])) {
      for ([key, value] of py.items(py.get(index, bucket, {}))) {
        if ((py.contains(String(key).toLowerCase(), normalized) || py.contains(String(py.toStr(value)).toLowerCase(), normalized))) {
          py.listAppend(matches, {"match": key, "value": value, "kind": bucket});
        }
      }
    }
  }
  return {"search_type": search_type, "term": term, "matches": py.sorted(matches, {key: ((item: any) => py.toStr(py.get(item, "match", ""))) as (item: any) => any}), "count": py.len(matches), "bounded": true};
}
