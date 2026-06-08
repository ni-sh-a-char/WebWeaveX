/**
 * Converted from Python: core/adaptive/dom_similarity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_NODES: any = 10000;
export function _nodeSignature(node: any): any {
  return py.join("|", [py.toStr(py.get(node, "tag", "")), py.slice(py.toStr(py.get(node, "text", "")), null, 200), py.toStr(py.get(node, "depth", 0))]);
}
export function computeDomSimilarity(left_nodes: any, right_nodes: any): any {
  var left: any = py.slice(left_nodes, null, MAX_NODES);
  var right: any = py.slice(right_nodes, null, MAX_NODES);
  var left_sigs: any = py.iter(left).map((node: any) => _nodeSignature(node));
  var right_sigs: any = py.iter(right).map((node: any) => _nodeSignature(node));
  var left_set: any = py.toSet(left_sigs);
  var right_set: any = py.toSet(right_sigs);
  var overlap: any = py.len(py.bitand(left_set, right_set));
  var union: any = py.max([py.len(py.bitor(left_set, right_set)), 1]);
  return {"score": py.div(overlap, union), "overlap": overlap, "left_count": py.len(left), "right_count": py.len(right), "bounded": true};
}
