/**
 * Converted from Python: core/knowledge/temporal_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function stampTemporalLineage(edge: any, tick: any): any {
  var lineage: any = py.or2(py.get(edge, "lineage", {}), () => ({}));
  var stages: any = ((Array.isArray(py.get(lineage, "stages"))) ? [...py.iter(py.get(lineage, "stages", []))] : []);
  py.listAppend(stages, {"stage": "temporal", "tick": tick});
  return {...(edge), "lineage": {...(lineage), "stages": stages, "tick": tick}};
}
