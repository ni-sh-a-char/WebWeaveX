/**
 * Converted from Python: core/adaptive/interaction_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { healSelector } from "./selectorHealingEngine.js";

export function recoverInteractionFlow(interactions: any, dom_nodes: any, html: any = ""): any {
  var recovered: any[] = [];
  var index: any;
  var action: any;
  for ([index, action] of py.enumerate(interactions)) {
    var selector: any = py.toStr(py.get(action, "selector", ""));
    var healed: any = healSelector(selector, dom_nodes, html);
    py.listAppend(recovered, {"step": index, "original_selector": selector, "healed_selector": py.get(healed, "healed_selector", selector), "strategy": py.get(healed, "strategy", "primary")});
  }
  return {"interactions": recovered, "bounded": true};
}
export { healSelector };
