/**
 * Converted from Python: core/ir/unified_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileUnifiedRuntimeIr(registry: any = null, graph: any = null, bus: any = null, phase_results: any = null, sources: any = null): any {
  registry = py.or2(registry, () => ({}));
  graph = py.or2(graph, () => ({}));
  bus = py.or2(bus, () => ([]));
  phase_results = py.or2(phase_results, () => ([]));
  sources = py.or2(sources, () => ({}));
  var phases: any = py.get(registry, "phases", {});
  return {"ir": "unified_runtime", "browser": _phasePayload(phases, sources, "browser"), "interaction": _phasePayload(phases, sources, "interaction"), "streaming": _phasePayload(phases, sources, "streaming"), "adaptive": _phasePayload(phases, sources, "adaptive"), "application": _phasePayload(phases, sources, "application"), "native": _phasePayload(phases, sources, "native"), "causality": _phasePayload(phases, sources, "causality"), "semantic": py.get(phases, "semantic", py.get(sources, "semantic", {})), "workflow": py.get(phases, "semantic", py.get(sources, "workflow", {})), "synchronization": py.get(phases, "synchronization", py.get(sources, "sync", {})), "evolution": _phasePayload(phases, sources, "evolution"), "connectors": _phasePayload(phases, sources, "connectors"), "memory": py.get(phases, "memory", py.get(sources, "memory", {})), "execution": py.get(phases, "execution", py.get(sources, "execution", {})), "reconstruction": py.get(phases, "reconstruction", py.get(sources, "reconstruction", {})), "runtime_graph": graph, "event_bus": py.sorted(bus, {key: ((item: any) => [py.get(item, "tick", 0), py.get(item, "order", 0)]) as (item: any) => any}), "phase_results": py.sorted(phase_results, {key: ((item: any) => py.toStr(py.get(item, "phase", ""))) as (item: any) => any}), "bounded": true};
}
export function _phasePayload(phases: any, sources: any, key: any): any {
  if (py.contains(phases, key)) {
    return (((py.at(phases, key) !== null && typeof py.at(phases, key) === "object" && !Array.isArray(py.at(phases, key)) && !(py.at(phases, key) instanceof Set) && !(py.at(phases, key) instanceof Map))) ? py.pyDict(py.at(phases, key)) : {"payload": py.at(phases, key)});
  }
  return py.pyDict(py.get(sources, key, {}));
}
export function unifiedRuntimeIrToGraph(unified_ir: any): any {
  var nodes: any = [{"id": "unified:root", "type": "unified_runtime"}];
  var edges: any[] = [];
  var graph: any = py.get(unified_ir, "runtime_graph", {});
  var node: any;
  for (node of py.iter(py.slice(py.get(graph, "nodes", []), null, 100000))) {
    var node_id: any = py.toStr(py.get(node, "id", ""));
    if (py.truthy(node_id)) {
      py.listAppend(nodes, py.pyDict(node));
      py.listAppend(edges, {"from": "unified:root", "to": node_id, "relation": "contains"});
    }
  }
  var phase: any;
  for (phase of py.iter(["semantic", "memory", "execution", "reconstruction", "synchronization"])) {
    if (py.truthy(py.get(unified_ir, phase))) {
      var pid: any = `phase:${py.toStr(phase)}`;
      py.listAppend(nodes, {"id": pid, "type": phase});
      py.listAppend(edges, {"from": pid, "to": "unified:root", "relation": "grounds"});
    }
  }
  return {"ir": "unified_runtime_graph", "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "edges": edges, "bounded": true};
}
