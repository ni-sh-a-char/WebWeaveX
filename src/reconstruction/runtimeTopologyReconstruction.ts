/**
 * Converted from Python: core/reconstruction/runtime_topology_reconstruction.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reconstructRuntimeTopology(runtime_graph: any = null, workers: any = null, connectors: any = null, execution_topology: any = null, sync_topology: any = null): any {
  var graph: any = py.or2(runtime_graph, () => ({}));
  var nodes: any = py.sorted(py.get(graph, "nodes", []), {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any});
  var edges: any = py.sorted(py.get(graph, "edges", []), {key: ((item: any) => [py.toStr(py.get(item, "from", "")), py.toStr(py.get(item, "to", "")), py.toStr(py.get(item, "relation", ""))]) as (item: any) => any});
  var worker_list: any = py.sorted(py.or2(workers, () => ([])), {key: ((item: any) => py.toStr(py.get(item, "worker_id", ""))) as (item: any) => any});
  var connector_list: any = py.sorted(py.or2(connectors, () => ([])), {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any});
  return {"distributed_workers": worker_list, "runtime_graph": {"nodes": nodes, "edges": edges}, "connector_topology": connector_list, "execution_topology": py.pyDict(py.or2(execution_topology, () => ({}))), "synchronization_topology": py.pyDict(py.or2(sync_topology, () => ({}))), "reconstructed": true, "bounded": true};
}
