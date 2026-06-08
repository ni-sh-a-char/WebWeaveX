/**
 * Converted from Python: core/documents/concept_transition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { parseSemanticDiscourse } from "./semanticDiscourseParser.js";

export function modelConceptTransitions(text: any): any {
  var d: any = parseSemanticDiscourse(text);
  var transitions: any[] = [];
  var e: any;
  for (e of py.iter(py.get(d, "transitions", []))) {
    if ((((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map))) && py.truthy(py.get(e, "from")) && py.truthy(py.get(e, "to")))) {
      py.listAppend(transitions, {"from": py.at(e, "from"), "to": py.at(e, "to"), "kind": "discourse"});
    }
  }
  return {"transitions": transitions, "count": py.len(transitions)};
}
export { parseSemanticDiscourse };
