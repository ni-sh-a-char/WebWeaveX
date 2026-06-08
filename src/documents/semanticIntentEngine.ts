/**
 * Converted from Python: core/documents/semantic_intent_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { structureCognition } from "../evidence/index.js";

let _INTENT_MARKERS: any = {"tutorial": ["step", "tutorial", "guide", "how to"], "reference": ["api", "reference", "parameter", "returns"], "architecture": ["architecture", "design", "component", "system"]};
export function classifySemanticIntent(text: any): any {
  var lower: any = String(py.or2(text, () => (""))).toLowerCase();
  var scores: any = Object.fromEntries(py.items(_INTENT_MARKERS).map(([k, markers]: any) => ([k, py.sum(py.iter(markers).filter((m: any) => py.contains(lower, m)).map((m: any) => 1))] as [any, any])));
  var best: any = (py.any(py.values(scores)) ? py.max(py.items(scores), {key: ((x: any) => py.at(x, 1)) as (item: any) => any}) : ["unknown", 0]);
  var observed: any = {"markers": scores};
  var inferred: any = {"intent": py.at(best, 0), "score": py.at(best, 1)};
  var reconciled: any = inferred;
  var amb: any = ((py.sum(py.values(scores).filter((v: any) => (v > 0)).map((v: any) => 1)) > 1) ? ["intent_ambiguous"] : []);
  return structureCognition(observed, inferred, reconciled, null, undefined, amb);
}
export { structureCognition };
