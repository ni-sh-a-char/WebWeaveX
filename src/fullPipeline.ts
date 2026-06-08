/**
 * Converted from Python: core/full_pipeline.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";
import { ENGINE_VERSION } from "./version.js";
import { runIntelligence } from "./intelligence/intelligenceEngine.js";
import { graphFingerprint } from "./crypto/kaalkaWrapper.js";

var KAALKA_AVAILABLE: any = true;
export let PIPELINE_VERSION: any = ENGINE_VERSION;
export function runPipeline(user_input: any, mode: any = "compiler"): any {
  var tokens: any = _tokenize(user_input);
  var nodes: any = _generateNodes(tokens);
  var relationships: any = _generateRelationships(tokens);
  var system: any = _deriveSystem(nodes, relationships);
  var execution_graph: any = _buildExecutionGraph(nodes, relationships);
  var execution_order: any = _deriveExecutionOrder(nodes);
  var spec: any = _buildSpec(nodes, relationships);
  var intelligence: Record<string, any> = {};
  intelligence = runIntelligence(execution_graph);
  var fingerprint: any = "";
  if (py.truthy(KAALKA_AVAILABLE)) {
    var fp_bytes: any = graphFingerprint(execution_graph);
    fingerprint = fp_bytes.hex();
  }
  var output: any = {"structured_data": {"system": system, "execution_graph": execution_graph, "execution_order": execution_order, "spec": spec, "intelligence": intelligence, "fingerprint": fingerprint}, "confidence": py.F(1.0), "source": "compiler", "version": PIPELINE_VERSION};
  return output;
}
export function _tokenize(user_input: any): any {
  if (!py.truthy(user_input)) {
    return [];
  }
  var tokens: any = String(user_input).toLowerCase();
  tokens = py.replace(py.replace(py.replace(tokens, ",", " "), "-", " "), "_", " ");
  tokens = py.replace(py.replace(py.replace(tokens, ".", " "), "(", " "), ")", " ");
  tokens = py.split(py.replace(tokens, "/", " "));
  return py.iter(tokens).filter((t: any) => py.truthy(t)).map((t: any) => t);
}
export function _generateNodes(tokens: any): any {
  var unique_tokens: any = py.sorted(py.toSet(tokens));
  var nodes: any = py.iter(unique_tokens).map((t: any) => ({"id": t}));
  return py.sorted(nodes, {key: ((x: any) => py.at(x, "id")) as (item: any) => any});
}
export function _generateRelationships(tokens: any): any {
  if (!py.truthy(tokens)) {
    return [];
  }
  var WINDOW: any = 3;
  var relationships: any[] = [];
  var i: any;
  for (i = 0; i < py.len(tokens); i++) {
    var j: any;
    for (j = py.max([0, py.sub(i, WINDOW)]); j < py.min([py.len(tokens), py.add(py.add(i, WINDOW), 1)]); j++) {
      if (!py.eq(i, j)) {
        py.listAppend(relationships, {"from": py.at(tokens, i), "to": py.at(tokens, j)});
      }
    }
  }
  var seen: Set<any> = new Set();
  var unique: any[] = [];
  var r: any;
  for (r of py.iter(relationships)) {
    var key: any = [py.at(r, "from"), py.at(r, "to")];
    if (!py.contains(seen, key)) {
      py.setAdd(seen, key);
      py.listAppend(unique, r);
    }
  }
  return py.sorted(unique, {key: ((x: any) => [py.at(x, "from"), py.at(x, "to")]) as (item: any) => any});
}
export function _deriveSystem(nodes: any, relationships: any): any {
  var components: any = py.sorted(py.iter(nodes).map((n: any) => ({"name": py.get(n, "id", "")})), {key: ((x: any) => py.at(x, "name")) as (item: any) => any});
  return {"system_type": "", "architecture": "", "components": components, "relationships": relationships};
}
export function _buildExecutionGraph(nodes: any, relationships: any): any {
  var edges: any = py.iter(relationships).map((r: any) => ({"from": py.get(r, "from", ""), "to": py.get(r, "to", "")}));
  return {"nodes": nodes, "edges": py.sorted(edges, {key: ((x: any) => [py.at(x, "from"), py.at(x, "to")]) as (item: any) => any})};
}
export function _deriveExecutionOrder(nodes: any): any {
  return py.sorted(py.iter(nodes).map((n: any) => py.get(n, "id", "")));
}
export function _buildSpec(nodes: any, relationships: any): any {
  return {"node_count": py.len(nodes), "edge_count": py.len(relationships)};
}
export { ENGINE_VERSION, graphFingerprint, runIntelligence };
