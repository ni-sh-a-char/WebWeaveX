/**
 * Converted from Python: core/documents/semantic_transition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelConceptTransitions } from "./conceptTransitionEngine.js";
import { parseRhetoricalStructure } from "./rhetoricalParserEngine.js";

export function modelSemanticTransitions(text: any): any {
  var trans: any = modelConceptTransitions(text);
  var rhet: any = parseRhetoricalStructure(text);
  var headings: any = py.iter(py.get(rhet, "units", [])).filter((u: any) => py.eq(py.get(u, "type"), "heading")).map((u: any) => u);
  var transitions: any = [...py.iter(py.get(trans, "transitions", []))];
  var i: any;
  for (i = 0; i < py.sub(py.len(headings), 1); i++) {
    py.listAppend(transitions, {"from": py.get(py.at(headings, i), "title", ""), "to": py.get(py.at(headings, py.add(i, 1)), "title", ""), "kind": "section_transition"});
  }
  return {"transitions": transitions, "count": py.len(transitions), "evidence": ["discourse:transitions"]};
}
export { modelConceptTransitions, parseRhetoricalStructure };
