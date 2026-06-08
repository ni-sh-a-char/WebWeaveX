/**
 * Converted from Python: core/documents/discourse_causality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildExplanationGraph } from "./explanationGraphEngine.js";

export function modelDiscourseCausality(text: any): any {
  var expl: any = buildExplanationGraph(text);
  var causal: any = py.iter(py.get(expl, "explains", [])).map((e: any) => ({"cause": py.get(e, "from"), "effect": py.get(e, "to")}));
  return {"causal": causal, "evidence": py.get(expl, "deterministic_inputs", [])};
}
export { buildExplanationGraph };
