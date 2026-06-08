/**
 * Converted from Python: core/documents/discourse_state_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function trackDiscourseState(sections: any): any {
  var ordered: any = py.sorted(sections, {key: ((s: any) => py.toInt(py.get(s, "order", 0))) as (item: any) => any});
  var current: any = (py.truthy(ordered) ? py.get(py.at(ordered, (-1)), "id") : null);
  return {"current_section": current, "depth": py.len(ordered), "deterministic": true};
}
