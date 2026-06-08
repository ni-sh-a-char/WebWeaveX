/**
 * Converted from Python: core/native/native_interaction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let ALLOWED_ACTIONS: any = py.toSet(new Set(["click", "focus", "type", "select", "scroll"]));
export function performNativeInteraction(action: any, target: any, value: any = "", step: any = 0): any {
  var normalized: any = py.strip(String(action).toLowerCase());
  if (!py.contains(ALLOWED_ACTIONS, normalized)) {
    return {"performed": false, "action": normalized, "error": "unsupported_action", "bounded": true};
  }
  return {"performed": true, "action": normalized, "target": target, "value": value, "step": step, "replay_index": step, "bounded": true};
}
export function buildInteractionSequence(interactions: any): any {
  var sequence: any[] = [];
  var index: any;
  var item: any;
  for ([index, item] of py.enumerate(py.slice(interactions, null, 10000))) {
    var result: any = performNativeInteraction(py.toStr(py.get(item, "action", "click")), py.toStr(py.get(item, "target", py.get(item, "selector", ""))), py.toStr(py.get(item, "value", "")), index);
    py.listAppend(sequence, result);
  }
  return sequence;
}
