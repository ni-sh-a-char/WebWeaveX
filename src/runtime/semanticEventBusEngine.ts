/**
 * Converted from Python: core/runtime/semantic_event_bus_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let MAX_EVENTS: any = 100000;
export class SemanticEventBus {
  declare _events: any;
  constructor() {
    this._events = py.deque([], MAX_EVENTS);
  }
  publish(event: any): any {
    py.listAppend(this._events, event);
  }
  consume(): any {
    if (!py.truthy(this._events)) {
      return null;
    }
    return py.popleft(this._events);
  }
}
