/**
 * Converted from Python: core/repository/architecture_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function inferArchitecture(topology: any, import_graph: any): any {
  var modules: any = py.get(topology, "modules", []);
  var layers: any = py.sorted(py.toSet(py.iter(modules).filter((m: any) => py.contains(m, "/")).map((m: any) => py.at(py.split(m, "/"), 0))));
  var components: any = py.sorted(py.toSet(py.iter(modules).map((m: any) => py.at(py.rsplit(m, "/", 1), (-1)))));
  var relationships: any = py.sorted(py.get(import_graph, "edges", []), {key: ((x: any) => [py.get(x, "from", ""), py.get(x, "to", "")]) as (item: any) => any});
  return {"layers": layers, "components": components, "relationships": relationships};
}
