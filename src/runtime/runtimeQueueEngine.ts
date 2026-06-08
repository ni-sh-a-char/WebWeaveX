/**
 * Converted from Python: core/runtime/runtime_queue_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let MAX_QUEUE: any = 1000;
export class RuntimeQueue {
  declare _q: any;
  declare _max: any;
  constructor(max_size: any = MAX_QUEUE) {
    this._q = py.deque([]);
    this._max = max_size;
  }
  enqueue(item: any): any {
    if ((py.len(this._q) >= this._max)) {
      return false;
    }
    py.listAppend(this._q, item);
    return true;
  }
  dequeue(): any {
    return (py.truthy(this._q) ? py.popleft(this._q) : null);
  }
  snapshot(): any {
    return [...py.iter(this._q)];
  }
}
