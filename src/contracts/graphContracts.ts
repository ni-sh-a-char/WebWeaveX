/**
 * Converted from Python: core/contracts/graph_contracts.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class RuntimeGraphContract {
  static normalize(graph: Record<string, any>): any {
    var nodes = [...py.iter(py.get(graph, "nodes", []))];
    var edges = [...py.iter(py.get(graph, "edges", []))];
    var nodes_sorted = py.sorted(nodes, {key: ((n) => [py.toStr(py.get(n, "id", "")), py.toStr(py.get(n, "type", "")), py.toStr(py.get(n, "name", ""))]) as (item: any) => any});
    var edges_sorted = py.sorted(edges, {key: ((e) => [py.toStr(py.get(e, "source", py.get(e, "from", ""))), py.toStr(py.get(e, "target", py.get(e, "to", ""))), py.toStr(py.get(e, "type", ""))]) as (item: any) => any});
    return {"nodes": nodes_sorted, "edges": edges_sorted, "bounded": true};
  }
}

/* ------------------------------------------------------------------ */
/* TypeScript-only contract types (runtime-invisible; hand-maintained) */
/* ------------------------------------------------------------------ */

export type RuntimeNode = Record<string, unknown> & { id?: string; type?: string; name?: string };
export type RuntimeEdge = Record<string, unknown> & {
  source?: string;
  from?: string;
  target?: string;
  to?: string;
  type?: string;
};

export type RuntimeGraph = {
  nodes: RuntimeNode[];
  edges: RuntimeEdge[];
  bounded?: boolean;
};
