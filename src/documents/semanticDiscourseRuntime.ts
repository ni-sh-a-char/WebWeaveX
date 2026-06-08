/**
 * Converted from Python: core/documents/semantic_discourse_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructTutorialCausality } from "./tutorialCausalityEngine.js";
import { modelDiscourseTransitions } from "./discourseTransitionEngine.js";

export function runDiscourseRuntime(sections: any): any {
  var tutorial: any = reconstructTutorialCausality(sections);
  var text: any = py.join("\n", py.iter(sections).map((s: any) => py.toStr(py.get(s, "content", ""))));
  var transitions: any = (py.truthy(sections) ? modelDiscourseTransitions(text) : {});
  return {"tutorial": tutorial, "transitions": transitions, "deterministic": true};
}
export { modelDiscourseTransitions, reconstructTutorialCausality };
