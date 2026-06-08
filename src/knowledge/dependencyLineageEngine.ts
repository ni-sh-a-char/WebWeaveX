/**
 * Converted from Python: core/knowledge/dependency_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildDependencyLineage(dependencies: any): any {
  var ordered: any = py.sorted(py.toSet(py.or2(dependencies, () => ([]))));
  var edges: any = py.range(py.max([0, py.sub(py.len(ordered), 1)])).map((i: any) => ({"from": py.at(ordered, i), "to": py.at(ordered, py.add(i, 1))}));
  return {"nodes": ordered, "edges": edges};
}
