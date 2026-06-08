/**
 * Converted from Python: core/repository/repository_file_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_EDGES: any = 100000;
export function buildRepositoryFileGraph(files: any, edges: any = null): any {
  var nodes: any[] = [];
  var file: any;
  for (file of py.iter(files)) {
    var path: any = py.at(file, "path");
    py.listAppend(nodes, {"id": path, "type": "file"});
  }
  var graph_edges: any = py.slice([...py.iter(py.or2(edges, () => ([])))], null, MAX_EDGES);
  return {"nodes": py.sorted(nodes, {key: ((x: any) => py.at(x, "id")) as (item: any) => any}), "edges": py.sorted(graph_edges, {key: ((x: any) => [py.toStr(py.get(x, "from")), py.toStr(py.get(x, "to"))]) as (item: any) => any}), "bounded": true};
}
