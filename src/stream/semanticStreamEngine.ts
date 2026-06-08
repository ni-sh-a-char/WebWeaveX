/**
 * Converted from Python: core/stream/semantic_stream_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_STREAM: any = 100000;
export class SemanticStream {
  declare events: any;
  constructor() {
    this.events = py.deque([]);
  }
  push(event: any): any {
    if ((py.len(this.events) >= MAX_STREAM)) {
      return;
    }
    py.listAppend(this.events, event);
  }
  next(): any {
    if (!py.truthy(this.events)) {
      return {"empty": true};
    }
    return py.popleft(this.events);
  }
}
