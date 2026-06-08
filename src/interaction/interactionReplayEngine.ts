/**
 * Converted from Python: core/interaction/interaction_replay_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { clickElement, fillInput, hoverElement, recordInteraction, selectOption, waitForSelector } from "./browserInteractionEngine.js";

export let MAX_REPLAY_ACTIONS: any = 1000;
let _ACTION_DISPATCH: any = {"click": (page: any, action: any) => clickElement(page, py.toStr(py.get(action, "selector", ""))), "fill": (page: any, action: any) => fillInput(page, py.toStr(py.get(action, "selector", "")), py.toStr(py.get(action, "value", py.get(py.get(action, "metadata", {}), "value", "")))), "select": (page: any, action: any) => selectOption(page, py.toStr(py.get(action, "selector", "")), py.toStr(py.get(action, "value", py.get(py.get(action, "metadata", {}), "value", "")))), "hover": (page: any, action: any) => hoverElement(page, py.toStr(py.get(action, "selector", ""))), "wait": (page: any, action: any) => waitForSelector(page, py.toStr(py.get(action, "selector", "")))};
export function replayInteractions(page: any, interaction_log: any): any {
  var replay_log: any[] = [];
  var index: any;
  var action: any;
  for ([index, action] of py.enumerate(py.slice(interaction_log, null, MAX_REPLAY_ACTIONS))) {
    var action_type: any = py.strip(py.toStr(py.get(action, "action", py.get(action, "type", ""))));
    var handler: any = py.get(_ACTION_DISPATCH, action_type);
    if ((handler !== null && handler !== undefined)) {
      handler(page, action);
    }
    py.listAppend(replay_log, {"step": index, "action": recordInteraction(action_type, py.toStr(py.get(action, "selector", "")), py.pyDict(py.get(action, "metadata", {})), index), "replayed": true});
  }
  return {"replay": replay_log, "bounded": true};
}
export { clickElement, fillInput, hoverElement, recordInteraction, selectOption, waitForSelector };
