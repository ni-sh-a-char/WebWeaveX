/**
 * Converted from Python: core/kernel/runtime_bus.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_BUS_EVENTS: any = 100000;
export function publishRuntimeEvent(bus: any, event_type: any, payload: any, tick: any = 0): any {
  var events: any = [...py.iter(bus)];
  py.listAppend(events, {"type": event_type, "tick": tick, "payload": py.pyDict(payload), "order": py.len(events)});
  events = py.slice(py.sorted(events, {key: ((item: any) => [py.at(item, "tick"), py.at(item, "order")]) as (item: any) => any}), null, MAX_BUS_EVENTS);
  return {"bus": events, "size": py.len(events), "bounded": true};
}
