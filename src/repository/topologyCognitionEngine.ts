/**
 * Converted from Python: core/repository/topology_cognition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { structureCognition } from "../evidence/index.js";
import { scoreSemanticConfidence } from "../evidence/semanticConfidenceEngine.js";
import { parseSource } from "../parsers/index.js";
import { assessTopologyEdgeFragility } from "./topologyFragilityEngine.js";
import { restrainTopologyEdge } from "./topologyRestraintEngine.js";

export function _edge(from_id: any, to_id: any, basis: any, evidence: any, parser_basis: any = null): any {
  var confidence: any = scoreSemanticConfidence(undefined, undefined, evidence);
  var observed: any = (py.eq(basis, "observed") ? {"from": from_id, "to": to_id} : {});
  var inferred: any = (py.contains(["inferred", "parser_derived"], basis) ? {"from": from_id, "to": to_id} : {});
  var unsupported: any = (py.truthy(evidence) ? {} : {"reason": "no_edge_evidence"});
  var edge_stub: any = {"evidence": evidence, "ambiguities": (py.truthy(evidence) ? [] : ["unsupported_topology_edge"]), "parser_basis": parser_basis};
  var fragility: any = assessTopologyEdgeFragility(edge_stub);
  py.setItem(confidence, "score", py.round(py.min([py.at(confidence, "score"), py.get(py.get(fragility, "confidence_limits", {}), "max_score", py.F(1.0))]), 3));
  var edge: any = {"from": from_id, "to": to_id, "metadata": {"edge_basis": basis}, "observed": observed, "inferred": inferred, "unsupported": unsupported, "fragility": fragility, "evidence": py.sorted(py.toSet(evidence)), "lineage": {"stage": "topology_edge", "basis": basis}, "confidence_basis": confidence, "confidence_limits": py.get(fragility, "confidence_limits", {}), "parser_basis": py.or2(parser_basis, () => ({})), "uncertainties": (py.truthy(evidence) ? {} : {"insufficient_evidence": true}), "ambiguities": (py.truthy(evidence) ? [] : ["unsupported_topology_edge"]), "contradictions": {}};
  return restrainTopologyEdge(edge);
}
export function buildTopologyCognition(text: any, path: any = "", observed_nodes: any = null, inferred_nodes: any = null): any {
  var parsed: any = (py.truthy(text) ? parseSource(py.or2(text, () => ("")), path) : null);
  var parser_nodes: any[] = [];
  var parser_edges: any[] = [];
  if (py.truthy(parsed)) {
    var sym: any = (((py.get(parsed, "symbols") !== null && typeof py.get(parsed, "symbols") === "object" && !Array.isArray(py.get(parsed, "symbols")) && !(py.get(parsed, "symbols") instanceof Set) && !(py.get(parsed, "symbols") instanceof Map))) ? py.get(parsed, "symbols", {}) : {});
    parser_nodes = py.slice(py.sorted(py.toSet(py.add(py.or2(py.get(sym, "classes", []), () => ([])), py.or2(py.get(sym, "functions", []), () => ([]))))), null, 30);
    var c: any;
    for (c of py.iter(py.or2(py.get(py.or2(py.get(parsed, "call_graph"), () => (py.get(parsed, "calls", {}))), "calls", []), () => ([])))) {
      if ((((c !== null && typeof c === "object" && !Array.isArray(c) && !(c instanceof Set) && !(c instanceof Map))) && py.truthy(py.get(c, "from")) && py.truthy(py.get(c, "to")))) {
        py.listAppend(parser_edges, _edge(py.toStr(py.at(c, "from")), py.toStr(py.at(c, "to")), "parser_derived", ["parser:call_graph"], {"source": path}));
      }
    }
  }
  var observed: any = {"topology": {"nodes": py.sorted(py.or2(observed_nodes, () => ([]))), "edges": []}};
  var parser_derived: any = {"topology": {"nodes": parser_nodes, "edges": parser_edges}};
  var inferred: any = {"topology": {"nodes": py.sorted(py.toSet(py.add(py.or2(inferred_nodes, () => ([])), parser_nodes))), "edges": parser_edges}};
  var reconciled: any = inferred;
  var ambiguities: any[] = [];
  if ((py.truthy(inferred_nodes) && !py.truthy(parser_nodes))) {
    py.listAppend(ambiguities, "inferred_topology_without_parser");
  }
  var out: any = structureCognition(observed, {"parser_derived": parser_derived, ...(inferred)}, reconciled, parsed, undefined, ambiguities);
  py.setItem(out, "topology_layers", {"observed": py.at(observed, "topology"), "parser_derived": py.at(parser_derived, "topology"), "inferred": py.at(inferred, "topology"), "reconciled": py.at(reconciled, "topology"), "ambiguous": ambiguities, "contradicted": py.get(out, "contradicted", {})});
  py.setItem(out, "runtime_causality", {"call_edges": parser_edges, "evidence": (py.truthy(parser_edges) ? ["parser:call_graph"] : [])});
  return out;
}
export { assessTopologyEdgeFragility, parseSource, restrainTopologyEdge, scoreSemanticConfidence, structureCognition };
