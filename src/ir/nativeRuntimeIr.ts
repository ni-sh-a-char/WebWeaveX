/**
 * Converted from Python: core/ir/native_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileNativeRuntimeIr(cognition: any): any {
  return {"ir": "native_runtime", "windows": py.get(cognition, "windows", {}), "accessibility_trees": py.get(cognition, "accessibility", {}), "runtime_graphs": py.get(cognition, "ui_graph", {}), "electron_state": py.get(cognition, "electron", {}), "terminal_streams": py.get(cognition, "terminal", {}), "vm_state": py.get(cognition, "vm", {}), "remote_sessions": py.get(cognition, "remote", {}), "desktop_runtime": py.get(cognition, "desktop", {}), "navigation": py.get(cognition, "navigation", {}), "streams": py.get(cognition, "streams", {}), "native_state": py.get(cognition, "native_state", {}), "bounded": true};
}
export function nativeRuntimeIrToGraph(native_ir: any): any {
  var ui_graph: any = py.get(native_ir, "runtime_graphs", {});
  var nodes: any = [...py.iter(py.get(ui_graph, "nodes", []))];
  var edges: any = [...py.iter(py.get(ui_graph, "edges", []))];
  if (!py.truthy(nodes)) {
    nodes = [{"id": "native:root", "type": "native"}];
  }
  var electron: any = py.get(native_ir, "electron_state", {});
  if (py.truthy(py.get(electron, "application"))) {
    py.listAppend(nodes, {"id": `electron:${py.toStr(py.at(electron, "application"))}`, "type": "electron"});
  }
  var terminal: any = py.get(native_ir, "terminal_streams", {});
  if (py.truthy(py.get(terminal, "stream_id"))) {
    py.listAppend(nodes, {"id": py.toStr(py.at(terminal, "stream_id")), "type": "terminal"});
  }
  var vm: any = py.get(native_ir, "vm_state", {});
  if (py.truthy(py.get(vm, "backend"))) {
    py.listAppend(nodes, {"id": `vm:${py.toStr(py.at(vm, "backend"))}`, "type": "vm"});
  }
  var remote: any = py.get(native_ir, "remote_sessions", {});
  if (py.truthy(py.get(remote, "protocol"))) {
    py.listAppend(nodes, {"id": `remote:${py.toStr(py.at(remote, "protocol"))}`, "type": "remote"});
  }
  return {"ir": "native_runtime_graph", "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "edges": edges, "bounded": true};
}
