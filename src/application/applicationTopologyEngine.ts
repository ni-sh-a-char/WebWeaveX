/**
 * Converted from Python: core/application/application_topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildApplicationTopology(workflow: any, navigation: any, dashboard: any): any {
  var nodes: any = [...py.iter(py.get(workflow, "nodes", []))];
  var menu: any;
  for (menu of py.iter(py.slice(py.get(navigation, "menus", []), null, 1000))) {
    py.listAppend(nodes, {"id": py.toStr(py.get(menu, "href", "")), "type": "nav_link"});
  }
  return {"nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "dashboard_widgets": py.len(py.get(dashboard, "widgets", [])), "bounded": true};
}
