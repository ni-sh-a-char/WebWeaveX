/**
 * Converted from Python: core/ir/streaming_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileStreamingIr(websocket_connections: any, websocket_events: any, dom_mutations: any, live_updates: any, sse_events: any, timeline: any, checkpoint: any): any {
  return {"ir": "streaming_runtime", "websocket_connections": websocket_connections, "stream_events": [...py.iter(py.get(timeline, "events", []))], "dom_mutations": dom_mutations, "live_update_graph": live_updates, "sse_events": sse_events, "replay_snapshots": {"checkpoint": checkpoint}, "runtime_timelines": timeline, "bounded": true};
}
export function streamingIrToRuntimeGraph(streaming_ir: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var event: any;
  for (event of py.iter(py.get(streaming_ir, "stream_events", []))) {
    var node_id: any = py.toStr(py.get(event, "id", ""));
    if (!py.truthy(node_id)) {
      continue;
    }
    py.listAppend(nodes, {"id": node_id, "type": "stream_event", "source": py.get(event, "source")});
  }
  var edge: any;
  for (edge of py.iter(py.get(py.get(streaming_ir, "runtime_timelines", {}), "edges", []))) {
    py.listAppend(edges, py.pyDict(edge));
  }
  return {"ir": "streaming_runtime_graph", "nodes": nodes, "edges": edges, "bounded": true};
}
