/**
 * Converted from Python: core/native/native_ui_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildNativeUiGraph(windows: any, accessibility: any, interactions: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var index: any;
  var window: any;
  for ([index, window] of py.enumerate(py.slice(py.get(windows, "windows", []), null, 5000))) {
    var window_id: any = py.toStr(py.get(window, "id", `window_${py.toStr(index)}`));
    py.listAppend(nodes, {"id": window_id, "type": "window", "title": py.toStr(py.get(window, "title", ""))});
  }
  var role: any;
  var bucket: any;
  for ([role, bucket] of py.iter([["button", "buttons"], ["form", "text_inputs"], ["tab", "tabs"], ["menu", "menus"], ["dialog", "dialogs"]])) {
    var element: any;
    for ([index, element] of py.enumerate(py.slice(py.get(accessibility, bucket, []), null, 5000))) {
      var element_id: any = py.toStr(py.get(element, "id", `${py.toStr(role)}_${py.toStr(index)}`));
      py.listAppend(nodes, {"id": element_id, "type": role, "name": py.toStr(py.get(element, "name", ""))});
    }
  }
  var focused: any = py.toStr(py.get(windows, "focused_window", ""));
  if (py.truthy(focused)) {
    py.listAppend(edges, {"from": "native:root", "to": focused, "relation": "focuses"});
  }
  var interaction: any;
  for ([index, interaction] of py.enumerate(py.slice(interactions, null, 10000))) {
    var action: any = py.toStr(py.get(interaction, "action", "activate"));
    var src: any = py.toStr(py.get(interaction, "from", `step_${py.toStr(index)}`));
    var dst: any = py.toStr(py.get(interaction, "to", `step_${py.toStr(py.add(index, 1))}`));
    var relation: any = "activates";
    if (py.eq(action, "click")) {
      relation = "opens";
    } else if (py.eq(action, "focus")) {
      relation = "focuses";
    } else if (py.contains(["navigate", "transition"], action)) {
      relation = "transitions";
    }
    py.listAppend(edges, {"from": src, "to": dst, "relation": relation});
  }
  if (!py.truthy(nodes)) {
    py.listAppend(nodes, {"id": "native:root", "type": "native"});
  }
  return {"nodes": py.sorted(nodes, {key: ((item: any) => py.at(item, "id")) as (item: any) => any}), "edges": py.sorted(edges, {key: ((item: any) => [py.get(item, "from", ""), py.get(item, "to", ""), py.get(item, "relation", "")]) as (item: any) => any}), "bounded": true};
}
