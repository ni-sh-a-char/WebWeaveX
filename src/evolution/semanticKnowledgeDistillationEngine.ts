/**
 * Converted from Python: core/evolution/semantic_knowledge_distillation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_DISTILLED: any = 5000;
export function distillSemanticKnowledge(records: any): any {
  var distilled: any[] = [];
  var record: any;
  for (record of py.iter(py.slice(records, null, MAX_DISTILLED))) {
    py.listAppend(distilled, py.sorted(py.keys(record)));
  }
  return {"distilled": distilled, "bounded": true};
}
