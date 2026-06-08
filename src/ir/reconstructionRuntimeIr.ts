/**
 * Converted from Python: core/ir/reconstruction_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileReconstructionRuntimeIr(reconstruction_payload: any): any {
  return {"ir": "reconstruction_runtime", "reconstructed_runtimes": py.get(reconstruction_payload, "runtime", {}), "replay_chains": py.get(py.get(reconstruction_payload, "replay", {}), "replay_chains", []), "topology": py.get(reconstruction_payload, "topology", {}), "runtime_identities": py.get(reconstruction_payload, "identity", {}), "fabricated_environments": py.get(reconstruction_payload, "fabrication", {}), "execution_continuity": py.get(reconstruction_payload, "state", {}), "validation": py.get(reconstruction_payload, "validation", {}), "browser": py.get(reconstruction_payload, "browser", {}), "application": py.get(reconstruction_payload, "application", {}), "timeline": py.get(reconstruction_payload, "timeline", {}), "clone": py.get(reconstruction_payload, "clone", {}), "bounded": true};
}
export function reconstructionRuntimeIrToGraph(reconstruction_ir: any): any {
  var nodes: any = [{"id": "reconstruction:root", "type": "reconstruction"}];
  var edges: any[] = [];
  var runtime: any = py.get(reconstruction_ir, "reconstructed_runtimes", {});
  var runtime_id: any = py.toStr(py.get(runtime, "runtime_id", ""));
  if (py.truthy(runtime_id)) {
    py.listAppend(nodes, {"id": `runtime:${py.toStr(runtime_id)}`, "type": "runtime"});
    py.listAppend(edges, {"from": "reconstruction:root", "to": `runtime:${py.toStr(runtime_id)}`, "relation": "reconstructs"});
  }
  var index: any;
  var chain: any;
  for ([index, chain] of py.enumerate(py.slice(py.get(reconstruction_ir, "replay_chains", []), null, 10000))) {
    var step_id: any = py.toStr(py.get(chain, "action_id", `step:${py.toStr(index)}`));
    var node_id: any = `replay:${py.toStr(step_id)}`;
    py.listAppend(nodes, {"id": node_id, "type": "replay"});
    py.listAppend(edges, {"from": node_id, "to": "reconstruction:root", "relation": "replays"});
  }
  var fabrication: any = py.get(reconstruction_ir, "fabricated_environments", {});
  if (py.truthy(py.get(fabrication, "fabricated"))) {
    py.listAppend(nodes, {"id": "fabrication:reality", "type": "fabrication"});
    py.listAppend(edges, {"from": "fabrication:reality", "to": "reconstruction:root", "relation": "fabricates"});
  }
  var clone: any = py.get(reconstruction_ir, "clone", {});
  if (py.truthy(py.get(clone, "cloned"))) {
    py.listAppend(nodes, {"id": "clone:environment", "type": "clone"});
    py.listAppend(edges, {"from": "clone:environment", "to": "reconstruction:root", "relation": "clones"});
  }
  var graph: any = py.get(py.get(reconstruction_ir, "topology", {}), "runtime_graph", {});
  var node: any;
  for (node of py.iter(py.slice(py.get(graph, "nodes", []), null, 5000))) {
    node_id = py.toStr(py.get(node, "id", ""));
    if (py.truthy(node_id)) {
      py.listAppend(nodes, {"id": node_id, "type": py.toStr(py.get(node, "type", "node"))});
    }
  }
  return {"ir": "reconstruction_runtime_graph", "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "edges": edges, "bounded": true};
}
