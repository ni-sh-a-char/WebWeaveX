/**
 * Converted from Python: core/memory/runtime_index_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeIndex(entities: any, workflows: any, graphs: any, streams: any, connectors: any): any {
  var entity_index: any = Object.fromEntries(py.iter(entities).filter((item: any) => (py.truthy(py.get(item, "id")) || py.truthy(py.get(item, "label")))).map((item: any) => ([py.toStr(py.get(item, "id", py.get(item, "label", ""))), item] as [any, any])));
  var workflow_index: any = Object.fromEntries(py.iter(workflows).map((item: any) => ([py.toStr(py.get(item, "id", py.get(item, "objective", ""))), item] as [any, any])));
  var graph_index: any = Object.fromEntries(py.enumerate(graphs).map(([index, graph]: any) => ([py.toStr(index), graph] as [any, any])));
  return {"entity_index": py.pyDict(py.sorted(py.items(entity_index))), "workflow_index": py.pyDict(py.sorted(py.items(workflow_index))), "graph_index": graph_index, "stream_index": Object.fromEntries(py.enumerate(streams).map(([index, stream]: any) => ([py.toStr(index), stream] as [any, any]))), "connector_index": Object.fromEntries(py.enumerate(connectors).map(([index, connector]: any) => ([py.toStr(index), connector] as [any, any]))), "bounded": true};
}
