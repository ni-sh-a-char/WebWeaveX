/**
 * Converted from Python: core/native/native_navigation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildNativeNavigation(desktop: any, electron: any = null): any {
  var routes: any[] = [];
  var app: any;
  for (app of py.iter(py.get(desktop, "active_apps", []))) {
    py.listAppend(routes, {"type": "app", "path": py.toStr(py.get(app, "name", ""))});
  }
  if (py.truthy(electron)) {
    var route: any;
    for (route of py.iter(py.get(electron, "routes", []))) {
      py.listAppend(routes, {"type": "electron_route", "path": py.toStr(route)});
    }
  }
  return {"routes": py.sorted(routes, {key: ((item: any) => py.at(item, "path")) as (item: any) => any}), "tabs": [...py.iter(py.get(desktop, "tabs", []))], "bounded": true};
}
