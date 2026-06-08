/**
 * Converted from Python: core/native/accessibility_tree_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let ROLE_MAP: any = {"button": "buttons", "textbox": "text_inputs", "edit": "text_inputs", "label": "labels", "menu": "menus", "menubar": "menus", "list": "lists", "tab": "tabs", "dialog": "dialogs"};
export function extractAccessibilityTree(snapshot: any = null, backend: any = null): any {
  var resolved_backend: any = py.or2(backend, () => (_resolveBackend()));
  if ((snapshot !== null && snapshot !== undefined)) {
    return _compileTree(snapshot, resolved_backend);
  }
  try {
    return _extractLiveTree(resolved_backend);
  } catch (_e: any) {
    return _emptyTree(resolved_backend, true);
  }
}
export function _resolveBackend(): any {
  if (py.eq(py.sysShim.platform, "win32")) {
    return "uia";
  }
  if (py.eq(py.sysShim.platform, "darwin")) {
    return "ax";
  }
  return "at-spi";
}
export function _compileTree(snapshot: any, backend: any): any {
  var nodes: any = py.slice([...py.iter(py.get(snapshot, "nodes", py.get(snapshot, "elements", [])))], null, 20000);
  var buckets: any = {"buttons": [], "text_inputs": [], "labels": [], "menus": [], "lists": [], "tabs": [], "dialogs": []};
  var node: any;
  for (node of py.iter(nodes)) {
    var role: any = String(py.toStr(py.get(node, "role", ""))).toLowerCase();
    var bucket: any = py.get(ROLE_MAP, role);
    if (py.truthy(bucket)) {
      py.listAppend(py.at(buckets, bucket), {"name": py.toStr(py.get(node, "name", "")), "id": py.toStr(py.get(node, "id", "")), "bounds": py.get(node, "bounds", {}), "enabled": py.truthy(py.get(node, "enabled", true))});
    }
  }
  return {...(buckets), "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "backend": backend, "bounded": true};
}
export function _extractLiveTree(backend: any): any {
  return _emptyTree(backend, true, "live_binding_unavailable");
}
export function _emptyTree(backend: any, degraded: any = false, reason: any = ""): any {
  return {"buttons": [], "text_inputs": [], "labels": [], "menus": [], "lists": [], "tabs": [], "dialogs": [], "nodes": [], "backend": backend, "degraded": degraded, "reason": reason, "bounded": true};
}
