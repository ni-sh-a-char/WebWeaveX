/**
 * Converted from Python: core/knowledge/ontology_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function stampOntologyLineage(edge: any, stage: any = "ontology"): any {
  var lineage: any = py.or2(py.get(edge, "lineage", {}), () => ({}));
  var stages: any = ((Array.isArray(py.get(lineage, "stages"))) ? [...py.iter(py.get(lineage, "stages", []))] : []);
  py.listAppend(stages, {"stage": stage, "from": py.get(edge, "from"), "to": py.get(edge, "to")});
  return {...(edge), "lineage": {...(lineage), "stages": stages, "depth": py.len(stages)}};
}
