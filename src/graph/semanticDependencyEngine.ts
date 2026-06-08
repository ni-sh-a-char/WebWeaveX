/**
 * Converted from Python: core/graph/semantic_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { structureCognition } from "../evidence/index.js";
import { parseSource } from "../parsers/index.js";

export function reconstructGraphDependencies(text: any, path: any = ""): any {
  var parsed: any = parseSource(py.or2(text, () => ("")), path);
  var graph: any = py.or2(py.get(parsed, "semantic_graph", {}), () => ({}));
  var edges: any = py.or2(py.get(graph, "edges", []), () => ([]));
  var deps: any = py.iter(edges).filter((e: any) => (((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map))) && py.truthy(py.get(e, "from")) && py.truthy(py.get(e, "to")))).map((e: any) => ({"from": py.get(e, "from"), "to": py.get(e, "to"), "basis": py.get(py.or2(py.get(e, "metadata"), () => ({})), "edge_basis", "observed")}));
  var observed: any = {"nodes": py.len(py.or2(py.get(graph, "nodes", []), () => ([])))};
  var inferred: any = {"graph_dependencies": deps};
  var reconciled: any = {"dependencies": deps};
  return structureCognition(observed, inferred, reconciled, parsed);
}
export { parseSource, structureCognition };
