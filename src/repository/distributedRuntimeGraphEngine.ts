/**
 * Converted from Python: core/repository/distributed_runtime_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildSemanticRuntimeGraph } from "./semanticRuntimeGraphEngine.js";

export function buildDistributedRuntimeGraph(source: any, path: any = "", files: any = null): any {
  var g: any = buildSemanticRuntimeGraph(source, path, files);
  var shards: Record<string, any> = {};
  var i: any;
  var node: any;
  for ([i, node] of py.enumerate(py.slice(py.get(g, "nodes", []), null, 20))) {
    py.setItem(shards, `shard_${py.toStr(py.mod(i, 4))}`, py.add(py.get(shards, `shard_${py.toStr(py.mod(i, 4))}`, []), [node]));
  }
  return {...(g), "shards": shards, "distributed": true, "evidence": py.get(g, "evidence", [])};
}
export { buildSemanticRuntimeGraph };
