/**
 * Converted from Python: core/runtime/semantic_replay_vm.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let MAX_REPLAY_EVENTS: any = 1000;
export function replaySemanticEvents(events: any): any {
  var replay_log: any[] = [];
  var ev: any;
  for (ev of py.iter(py.slice(events, null, MAX_REPLAY_EVENTS))) {
    py.listAppend(replay_log, {"event": py.get(ev, "id"), "type": py.get(ev, "type")});
  }
  return {"replay_log": replay_log, "event_count": py.len(replay_log), "bounded": true};
}
