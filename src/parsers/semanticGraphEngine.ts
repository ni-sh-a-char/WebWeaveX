/**
 * Converted from Python: core/parsers/semantic_graph_engine.py
 * Hand-fixed production module (protected): the generated version used
 * tuple-valued dict keys, which coerce to "f,t" strings on plain JS objects
 * and then destructure as characters — yielding zero edges. Edge metadata is
 * now keyed by a JSON-encoded pair with the original pair kept alongside,
 * preserving Python's tuple-sort and keep-if-present semantics exactly.
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_GRAPH_NODES: any = 5000;
export let MAX_GRAPH_EDGES: any = 20000;

export function buildSemanticGraph(parsed: any): any {
  const symbols: any = py.or2(py.get(parsed, "symbols", {}), () => ({}));
  const imports: any = py.or2(py.get(parsed, "imports", {}), () => ({}));
  const calls: any = py.or2(py.get(parsed, "calls", {}), () => ({}));
  const source_id: any = py.toStr(
    py.or2(py.get(parsed, "source_id"), () =>
      py.or2(py.get(parsed, "language"), () => "module"),
    ),
  );
  const node_ids: Set<string> = new Set([source_id]);
  for (const key of ["classes", "functions", "interfaces", "symbols"]) {
    for (const name of py.or2(py.get(symbols, key, []), () => []) as any[]) {
      node_ids.add(py.toStr(name));
    }
  }
  const isDict = (e: any) =>
    e !== null && typeof e === "object" && !Array.isArray(e) &&
    !(e instanceof Set) && !(e instanceof Map);
  for (const edge of py.or2(py.get(imports, "edges", []), () => []) as any[]) {
    if (isDict(edge)) node_ids.add(py.toStr(py.get(edge, "to", "")));
  }

  const edge_meta: Map<string, { pair: [string, string]; basis: string }> =
    new Map();
  for (const edge of py.or2(py.get(imports, "edges", []), () => []) as any[]) {
    if (isDict(edge) && py.truthy(py.get(edge, "from")) && py.truthy(py.get(edge, "to"))) {
      const pair: [string, string] = [py.toStr(edge["from"]), py.toStr(edge["to"])];
      edge_meta.set(JSON.stringify(pair), { pair, basis: "observed" });
    }
  }
  for (const edge of py.or2(py.get(calls, "calls", []), () => []) as any[]) {
    if (isDict(edge) && py.truthy(py.get(edge, "from")) && py.truthy(py.get(edge, "to"))) {
      const f = py.toStr(edge["from"]);
      const t = py.toStr(edge["to"]);
      node_ids.add(f);
      node_ids.add(t);
      const k = JSON.stringify([f, t]);
      // Python: keep existing meta if present, else "observed".
      if (!edge_meta.has(k)) edge_meta.set(k, { pair: [f, t], basis: "observed" });
    }
  }

  const nodes: any[] = py
    .slice(py.sorted([...node_ids].filter((n) => py.truthy(n))), null, MAX_GRAPH_NODES)
    .map((nid: any) => ({ id: nid, kind: "symbol", metadata: {} }));
  const allowed = new Set(nodes.map((n: any) => n.id));
  // Python sorts the (from, to) tuples lexicographically by element.
  const sortedPairs = [...edge_meta.values()].sort((a, b) => {
    const f = a.pair[0] < b.pair[0] ? -1 : a.pair[0] > b.pair[0] ? 1 : 0;
    if (f !== 0) return f;
    return a.pair[1] < b.pair[1] ? -1 : a.pair[1] > b.pair[1] ? 1 : 0;
  });
  const edge_list: any[] = [];
  for (const { pair, basis } of sortedPairs) {
    if (edge_list.length >= MAX_GRAPH_EDGES) break;
    if (allowed.has(pair[0]) && allowed.has(pair[1])) {
      edge_list.push({
        from: pair[0],
        to: pair[1],
        metadata: { edge_basis: basis, evidence: ["parser:graph"] },
      });
    }
  }
  return { nodes, edges: edge_list, max_edges: MAX_GRAPH_EDGES };
}
