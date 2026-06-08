/**
 * Converted from Python: core/repository/service_runtime_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { inferServiceInteractions } from "./serviceInteractionEngine.js";
import { parseSource } from "../parsers/parserRegistry.js";

export function buildServiceRuntimeGraph(source: any, path: any = "", files: any = null): any {
  var parsed: any = (py.truthy(source) ? parseSource(source, path) : {});
  var interactions: any = inferServiceInteractions(parsed, py.or2(files, () => ([])));
  var nodes: any = py.sorted(py.toSet(py.iter(py.get(interactions, "interactions", [])).filter((i: any) => py.truthy(py.get(i, "from"))).map((i: any) => py.get(i, "from"))));
  nodes = py.add(nodes, py.sorted(py.toSet(py.iter(py.get(interactions, "interactions", [])).filter((i: any) => py.truthy(py.get(i, "to"))).map((i: any) => py.get(i, "to")))));
  return {"nodes": py.slice(py.sorted(py.toSet(py.iter(nodes).filter((n: any) => py.truthy(n)).map((n: any) => py.toStr(n)))), null, 200), "edges": py.slice(py.get(interactions, "interactions", []), null, 200), "service_files": py.get(interactions, "service_files", []), "evidence": py.get(interactions, "evidence", [])};
}
export { inferServiceInteractions, parseSource };
