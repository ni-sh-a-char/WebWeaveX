/**
 * Converted from Python: core/semantic/semantic_diff_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function diffSemanticRuntime(previous: any, current: any): any {
  var prev_entities: any = py.toSet(py.iter(py.get(py.get(previous, "entities", {}), "entities", [])).map((item: any) => py.toStr(py.get(item, "id", ""))));
  var curr_entities: any = py.toSet(py.iter(py.get(py.get(current, "entities", {}), "entities", [])).map((item: any) => py.toStr(py.get(item, "id", ""))));
  var prev_domain: any = py.get(py.get(previous, "domain", {}), "domain", "");
  var curr_domain: any = py.get(py.get(current, "domain", {}), "domain", "");
  return {"entities_added": py.sorted(py.sub(curr_entities, prev_entities)), "entities_removed": py.sorted(py.sub(prev_entities, curr_entities)), "domain_changed": !py.eq(prev_domain, curr_domain), "ontology_evolved": !py.eq(py.get(previous, "ontology"), py.get(current, "ontology")), "workflow_mutated": !py.eq(py.get(previous, "workflow"), py.get(current, "workflow")), "bounded": true};
}
