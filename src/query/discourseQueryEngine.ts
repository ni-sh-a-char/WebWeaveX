/**
 * Converted from Python: core/query/discourse_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function queryDiscourseSections(sections: any, section_id: any): any {
  var match: any = py.next(py.iter(py.iter(sections).filter((s: any) => py.eq(py.get(s, "id"), section_id)).map((s: any) => s)), null);
  return {"section": match, "found": (match !== null && match !== undefined), "deterministic": true};
}
