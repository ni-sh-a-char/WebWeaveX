/**
 * Converted from Python: core/internet/source_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildLineage } from "../evidence/lineageEngine.js";

export function reconstructSourceLineage(sources: any): any {
  var ordered: any = py.sorted(py.toSet(py.iter(py.or2(sources, () => ([]))).filter((s: any) => py.truthy(s)).map((s: any) => py.toStr(s))));
  var lineage: any = buildLineage([{"stage": "source_lineage", "inputs": [], "outputs": ordered}]);
  return {"sources": ordered, "lineage": lineage, "evidence": ["source_lineage"]};
}
export { buildLineage };
