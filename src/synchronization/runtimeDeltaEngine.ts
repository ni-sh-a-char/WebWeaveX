/**
 * Converted from Python: core/synchronization/runtime_delta_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeDelta(previous: any = null, current: any = null, tick: any = 0): any {
  previous = py.or2(previous, () => ({}));
  current = py.or2(current, () => ({}));
  var changes: any[] = [];
  var key: any;
  for (key of py.iter(py.sorted(py.bitor(py.toSet(py.keys(previous)), py.toSet(py.keys(current)))))) {
    if (!py.eq(py.get(previous, key), py.get(current, key))) {
      py.listAppend(changes, {"field": key, "from": py.get(previous, key), "to": py.get(current, key), "kind": _classifyChange(key)});
    }
  }
  var payload: any = jsonKey(changes);
  var delta_id: any = py.slice(py.hashNew("sha256", py.encode(payload, "utf-8")).hexdigest(), null, 32);
  return {"delta_id": delta_id, "changes": changes, "timestamp": tick, "bounded": true};
}
export function _classifyChange(field: any): any {
  if (py.contains(field, "semantic")) {
    return "semantic_change";
  }
  if (py.contains(field, "workflow")) {
    return "workflow_change";
  }
  if ((py.contains(field, "dom") || py.contains(field, "ui"))) {
    return "ui_mutation";
  }
  if (py.contains(field, "state")) {
    return "application_state_mutation";
  }
  return "runtime_transition";
}
export function jsonKey(changes: any): any {
  var parts: any = py.iter(py.sorted(changes, {key: ((item: any) => py.at(item, "field")) as (item: any) => any})).map((c: any) => `${py.toStr(py.at(c, "field"))}:${py.toStr(py.at(c, "kind"))}`);
  return py.join("|", parts);
}
