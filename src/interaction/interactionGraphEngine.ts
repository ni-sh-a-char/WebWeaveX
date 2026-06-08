/**
 * Converted from Python: core/interaction/interaction_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaHashEngine.js";

export let MAX_GRAPH_NODES: any = 10000;
export let MAX_GRAPH_EDGES: any = 50000;
export function buildInteractionGraph(interactions: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var previous_id: any = "state_root";
  py.listAppend(nodes, {"id": previous_id, "type": "state", "name": "root"});
  var index: any;
  var interaction: any;
  for ([index, interaction] of py.enumerate(py.slice(interactions, null, MAX_GRAPH_NODES))) {
    var node_id: any = py.toStr(py.get(interaction, "id", `interaction_${py.toStr(index)}`));
    var action: any = py.toStr(py.get(interaction, "action", ""));
    var selector: any = py.toStr(py.get(interaction, "selector", ""));
    var node_type: any = (py.eq(action, "fill") ? "form" : "page");
    if (py.contains(String(selector).toLowerCase(), "modal")) {
      node_type = "modal";
    }
    if (py.contains(String(selector).toLowerCase(), "tab")) {
      node_type = "tab";
    }
    py.listAppend(nodes, {"id": node_id, "type": node_type, "action": action, "selector": selector});
    var relation: any = py.or2(action, () => ("transition"));
    if (py.eq(action, "click")) {
      relation = "click";
    } else if (py.contains(new Set(["fill", "select"]), action)) {
      relation = "submission";
    } else if (py.eq(action, "wait")) {
      relation = "navigation";
    }
    py.listAppend(edges, {"from": previous_id, "to": node_id, "relation": relation});
    previous_id = node_id;
  }
  var graph: any = {"ir": "interaction_graph", "nodes": py.slice(nodes, null, MAX_GRAPH_NODES), "edges": py.slice(edges, null, MAX_GRAPH_EDGES), "graph_hash": computeKaalkaHashPayload({"nodes": py.slice(nodes, null, MAX_GRAPH_NODES), "edges": py.slice(edges, null, MAX_GRAPH_EDGES)}), "bounded": true};
  return graph;
}
export function interactionGraphToRuntimeIr(graph: any): any {
  return {"ir": "interaction_runtime", "nodes": [...py.iter(py.get(graph, "nodes", []))], "edges": [...py.iter(py.get(graph, "edges", []))], "bounded": true};
}
export { computeKaalkaHashPayload };
