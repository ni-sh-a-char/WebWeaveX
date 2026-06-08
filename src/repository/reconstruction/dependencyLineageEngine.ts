/**
 * Converted from Python: core/repository/reconstruction/dependency_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildDependencyLineage(deps: any): any {
  var d: any = py.sorted(py.toSet(py.or2(deps, () => ([]))));
  var edges: any = py.range(py.max([0, py.sub(py.len(d), 1)])).map((i: any) => ({"from": py.at(d, i), "to": py.at(d, py.add(i, 1))}));
  return {"nodes": d, "edges": edges};
}
