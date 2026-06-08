/**
 * Converted from Python: core/ir/live_runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileLiveRuntimeIr(live: any): any {
  return {"ir": "live_runtime", "database_topology": py.get(live, "database", {}), "api_topology": py.get(live, "api", {}), "stream_lineage": py.get(live, "streams", {}), "filesystem": py.get(live, "filesystem", {}), "containers": py.get(live, "containers", {}), "kubernetes": py.get(live, "kubernetes", {}), "cicd": py.get(live, "cicd", {}), "telemetry": py.get(live, "telemetry", {}), "ide": py.get(live, "ide", {}), "graph": py.get(live, "graph", {}), "synchronization": py.get(live, "sync_state", {}), "bounded": true};
}
export function liveRuntimeIrToGraph(live_ir: any): any {
  var graph: any = py.get(live_ir, "graph", {});
  var nodes: any = [...py.iter(py.get(graph, "nodes", []))];
  var edges: any = [...py.iter(py.get(graph, "edges", []))];
  if (!py.truthy(nodes)) {
    nodes = [{"id": "live:root", "type": "live_runtime"}];
  }
  var k8s: any = py.get(live_ir, "kubernetes", {});
  var deploy: any;
  for (deploy of py.iter(py.slice(py.get(k8s, "deployments", []), null, 1000))) {
    var name: any = py.toStr((((deploy !== null && typeof deploy === "object" && !Array.isArray(deploy) && !(deploy instanceof Set) && !(deploy instanceof Map))) ? py.get(deploy, "name", deploy) : deploy));
    py.listAppend(nodes, {"id": `k8s:deploy:${py.toStr(name)}`, "type": "deployment"});
  }
  var stream: any;
  for (stream of py.iter(py.slice(py.get(py.get(live_ir, "stream_lineage", {}), "streams", []), null, 1000))) {
    var topics: any = py.get(stream, "topics", []);
    if (py.truthy(topics)) {
      py.listAppend(nodes, {"id": `stream:${py.toStr(py.get(stream, "stream_type", "unknown"))}:${py.toStr(py.at(topics, 0))}`, "type": "stream"});
    }
  }
  return {"ir": "live_runtime_graph", "nodes": py.sorted(nodes, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "edges": edges, "bounded": true};
}
export function buildLiveTopologyGraph(live: any): any {
  var nodes: any = [{"id": "live:root", "type": "live_runtime"}];
  var edges: any[] = [];
  var db: any = py.get(live, "database", {});
  if (py.truthy(py.get(db, "tables"))) {
    var db_id: any = `db:${py.toStr(py.get(db, "database_type", "db"))}`;
    py.listAppend(nodes, {"id": db_id, "type": "database"});
    py.listAppend(edges, {"from": "live:root", "to": db_id, "relation": "connects"});
  }
  var api: any = py.get(live, "api", {});
  if (py.truthy(py.get(api, "endpoints"))) {
    var api_id: any = `api:${py.toStr(py.get(api, "api_type", "rest"))}`;
    py.listAppend(nodes, {"id": api_id, "type": "api"});
    py.listAppend(edges, {"from": "live:root", "to": api_id, "relation": "exposes"});
  }
  var containers: any = py.get(live, "containers", {});
  var container: any;
  for (container of py.iter(py.slice(py.get(containers, "containers", []), null, 1000))) {
    var cid: any = py.toStr((((container !== null && typeof container === "object" && !Array.isArray(container) && !(container instanceof Set) && !(container instanceof Map))) ? py.get(container, "id", container) : container));
    py.listAppend(nodes, {"id": `container:${py.toStr(cid)}`, "type": "container"});
    py.listAppend(edges, {"from": "live:root", "to": `container:${py.toStr(cid)}`, "relation": "runs"});
  }
  var k8s: any = py.get(live, "kubernetes", {});
  var pod: any;
  for (pod of py.iter(py.slice(py.get(k8s, "pods", []), null, 1000))) {
    var pid: any = py.toStr((((pod !== null && typeof pod === "object" && !Array.isArray(pod) && !(pod instanceof Set) && !(pod instanceof Map))) ? py.get(pod, "name", pod) : pod));
    py.listAppend(nodes, {"id": `pod:${py.toStr(pid)}`, "type": "pod"});
    py.listAppend(edges, {"from": "live:root", "to": `pod:${py.toStr(pid)}`, "relation": "schedules"});
  }
  return {"nodes": py.sorted(nodes, {key: ((item: any) => py.at(item, "id")) as (item: any) => any}), "edges": py.sorted(edges, {key: ((item: any) => [py.get(item, "from", ""), py.get(item, "to", "")]) as (item: any) => any}), "bounded": true};
}
