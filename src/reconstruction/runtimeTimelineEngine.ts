/**
 * Converted from Python: core/reconstruction/runtime_timeline_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeTimeline(events: any = null, actions: any = null, mutations: any = null, synchronization: any = null, execution: any = null, recovery: any = null, replay: any = null, tick: any = 0): any {
  var timeline: any[] = [];
  var kind: any;
  var items: any;
  for ([kind, items] of py.iter([["event", py.or2(events, () => ([]))], ["action", py.or2(actions, () => ([]))], ["mutation", py.or2(mutations, () => ([]))], ["sync", py.or2(synchronization, () => ([]))], ["execution", py.or2(execution, () => ([]))], ["recovery", py.or2(recovery, () => ([]))], ["replay", py.or2(replay, () => ([]))]])) {
    var index: any;
    var item: any;
    for ([index, item] of py.enumerate(items)) {
      py.listAppend(timeline, {"kind": kind, "tick": py.toInt(py.get(item, "tick", py.add(tick, index))), "id": py.toStr(py.get(item, "id", `${py.toStr(kind)}:${py.toStr(index)}`)), "payload": py.pyDict(item)});
    }
  }
  var ordered: any = py.sorted(timeline, {key: ((item: any) => [py.at(item, "tick"), py.at(item, "kind"), py.at(item, "id")]) as (item: any) => any});
  return {"timeline": ordered, "count": py.len(ordered), "replay_deterministic": true, "bounded": true};
}
