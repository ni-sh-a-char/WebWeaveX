/**
 * Converted from Python: core/evidence/semantic_confidence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function scoreSemanticConfidence(parsed: any = null, graph: any = null, extra_evidence: any = null): any {
  var inputs: any[] = [];
  var evidence: any[] = [];
  var score: any = py.F(0.2);
  if (((parsed !== null && typeof parsed === "object" && !Array.isArray(parsed) && !(parsed instanceof Set) && !(parsed instanceof Map)))) {
    var flags: any = py.get(parsed, "evidence", {});
    if (((flags !== null && typeof flags === "object" && !Array.isArray(flags) && !(flags instanceof Set) && !(flags instanceof Map)))) {
      var key: any;
      var val: any;
      for ([key, val] of py.iter(py.sorted(py.items(flags)))) {
        py.listAppend(inputs, `parser.${py.toStr(key)}=${py.toStr(py.truthy(val))}`);
        if (py.truthy(val)) {
          py.listAppend(evidence, `parser:${py.toStr(key)}`);
          score = py.add(score, py.F(0.12));
        }
      }
    }
  }
  if (((graph !== null && typeof graph === "object" && !Array.isArray(graph) && !(graph instanceof Set) && !(graph instanceof Map)))) {
    var nodes: any = py.or2(py.get(graph, "nodes", []), () => ([]));
    var edges: any = py.or2(py.get(graph, "edges", []), () => ([]));
    py.listAppend(inputs, `graph.nodes=${py.toStr(py.len(nodes))}`);
    py.listAppend(inputs, `graph.edges=${py.toStr(py.len(edges))}`);
    if (py.truthy(edges)) {
      py.listAppend(evidence, "graph:edges");
      score = py.add(score, py.min([py.F(0.25), py.mul(py.len(edges), py.F(0.01))]));
    }
  }
  var e: any;
  for (e of py.iter(py.or2(extra_evidence, () => ([])))) {
    py.listAppend(evidence, py.toStr(e));
    score = py.add(score, py.F(0.05));
  }
  score = py.round(py.min([py.F(1.0), py.max([py.F(0.0), score])]), 3);
  return {"score": score, "basis": {"parser_density": py.len(py.iter(evidence).filter((e: any) => py.truthy(py.startswith(e, "parser:"))).map((e: any) => e)), "graph_edges": (py.truthy(graph) ? py.len(py.or2(py.get(py.or2(graph, () => ({})), "edges", []), () => ([]))) : 0)}, "evidence": py.sorted(py.toSet(evidence)), "deterministic_inputs": py.sorted(inputs)};
}
