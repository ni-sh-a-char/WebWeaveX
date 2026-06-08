/**
 * Converted from Python: core/internet/lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildSourceLineage(chain: any): any {
  var ordered: any = py.iter(py.or2(chain, () => ([]))).filter((u: any) => py.truthy(u)).map((u: any) => py.toStr(u));
  var edges: any = py.range(py.sub(py.len(ordered), 1)).map((i: any) => ({"from": py.at(ordered, i), "to": py.at(ordered, py.add(i, 1))}));
  return {"chain": ordered, "edges": edges, "depth": py.len(ordered)};
}
