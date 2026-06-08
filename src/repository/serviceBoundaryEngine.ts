/**
 * Converted from Python: core/repository/service_boundary_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { structureCognition } from "../evidence/index.js";
import { parseSource } from "../parsers/index.js";

export function inferServiceBoundariesFromText(text: any, path: any = ""): any {
  var parsed: any = parseSource(text, path);
  var symbol_data: any = py.get(parsed, "symbols", {});
  if ((Array.isArray(symbol_data))) {
    var classes: any = symbol_data;
  } else {
    classes = (((symbol_data !== null && typeof symbol_data === "object" && !Array.isArray(symbol_data) && !(symbol_data instanceof Set) && !(symbol_data instanceof Map))) ? py.get(symbol_data, "classes", []) : []);
  }
  var calls: any = py.get(py.or2(py.get(parsed, "call_graph"), () => (py.get(parsed, "calls", {}))), "calls", []);
  var api: any = py.or2(py.get(parsed, "api_evidence"), () => (py.get(parsed, "api_surface", {})));
  var observed: any = {"services": py.sorted(py.iter(classes).filter((n: any) => py.any(py.iter(["service", "worker", "handler", "controller"]).map((h: any) => py.contains(String(py.toStr(n)).toLowerCase(), h)))).map((n: any) => n)), "call_edges": py.len(calls), "api_routes": (((api !== null && typeof api === "object" && !Array.isArray(api) && !(api instanceof Set) && !(api instanceof Map))) ? py.get(api, "routes", []) : [])};
  var inferred: any = {"services": py.slice(py.sorted(classes), null, 10), "call_edges": py.len(calls)};
  var reconciled: any = {"services": py.or2(py.at(observed, "services"), () => (py.at(inferred, "services"))), "call_edges": py.at(observed, "call_edges"), "api_routes": py.at(observed, "api_routes")};
  var out: any = structureCognition(observed, inferred, reconciled, parsed);
  var cognition: any = py.and2(parsed, () => ({"parser_evidence": py.get(out, "evidence", []), "semantic_evidence": py.iter(py.get(reconciled, "services", [])).map((s: any) => `service:${py.toStr(s)}`), "graph_evidence": py.range(py.get(observed, "call_edges", 0)).map((i: any) => `call_edge:${py.toStr(i)}`), "lineage": py.get(out, "lineage", {})}));
  py.setItem(out, "services", py.get(reconciled, "services", []));
  py.setItem(out, "boundaries", py.get(reconciled, "boundaries", []));
  py.setItem(out, "topology_layers", {"observed": observed, "parser_derived": {"services": py.get(inferred, "services", []), "calls": py.get(observed, "call_edges", 0)}, "inferred": inferred, "reconciled": reconciled, "ambiguous": py.get(out, "ambiguities", []), "contradicted": py.get(out, "contradicted", {})});
  if (py.truthy(cognition)) {
    py.update(out, Object.fromEntries(py.items(cognition).filter(([k, v]: any) => !py.contains(out, k)).map(([k, v]: any) => ([k, v] as [any, any]))));
  }
  return out;
}
export function inferServiceBoundariesFromPaths(paths: any): any {
  var groups: Record<string, any> = {};
  var p: any;
  for (p of py.iter(py.sorted(py.toSet(py.or2(paths, () => ([])))))) {
    var key: any = (py.contains(p, "/") ? py.at(py.split(p, "/"), 0) : py.at(py.split(p, "\\"), 0));
    py.listAppend(py.setdefault(groups, key, []), p);
  }
  var observed: any = {"boundaries": py.iter(py.sorted(py.items(groups))).map(([k, v]: any) => ({"service": k, "paths": py.sorted(v)}))};
  var out: any = structureCognition(observed, observed, observed, null);
  py.setItem(out, "boundaries", py.get(observed, "boundaries", []));
  return out;
}
export function inferServiceBoundaries(text_or_paths: any, path: any = ""): any {
  if ((Array.isArray(text_or_paths))) {
    return inferServiceBoundariesFromPaths(text_or_paths);
  }
  return inferServiceBoundariesFromText(text_or_paths, path);
}
export { parseSource, structureCognition };
