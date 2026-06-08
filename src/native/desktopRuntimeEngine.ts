/**
 * Converted from Python: core/native/desktop_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildDesktopRuntime(windows: any, accessibility: any, snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  var window_list: any = [...py.iter(py.get(windows, "windows", []))];
  var active_apps: any[] = [];
  var seen: Set<any> = new Set();
  var window: any;
  for (window of py.iter(window_list)) {
    var app_name: any = py.toStr(py.get(window, "application", py.get(window, "app", "")));
    if ((py.truthy(app_name) && !py.contains(seen, app_name))) {
      py.setAdd(seen, app_name);
      py.listAppend(active_apps, {"name": app_name, "windows": 1});
    }
  }
  var app: any;
  for (app of py.iter(py.get(snap, "active_apps", []))) {
    var name: any = py.toStr(py.get(app, "name", ""));
    if ((py.truthy(name) && !py.contains(seen, name))) {
      py.listAppend(active_apps, app);
    }
  }
  return {"active_apps": py.sorted(active_apps, {key: ((item: any) => py.at(item, "name")) as (item: any) => any}), "runtime_state": {"focused_window": py.get(windows, "focused_window", ""), "window_count": py.len(window_list)}, "windows": window_list, "tabs": [...py.iter(py.get(snap, "tabs", []))], "dialogs": [...py.iter(py.get(accessibility, "dialogs", []))], "notifications": [...py.iter(py.get(snap, "notifications", []))], "bounded": true};
}
