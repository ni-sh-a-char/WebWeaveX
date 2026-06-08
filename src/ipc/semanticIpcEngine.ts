/**
 * Converted from Python: core/ipc/semantic_ipc_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_MESSAGES: any = 10000;
export class SemanticIPC {
  declare queue: any;
  constructor() {
    this.queue = py.deque([]);
  }
  send(message: any): any {
    if ((py.len(this.queue) >= MAX_MESSAGES)) {
      return;
    }
    py.listAppend(this.queue, message);
  }
  receive(): any {
    if (!py.truthy(this.queue)) {
      return {"empty": true};
    }
    return py.popleft(this.queue);
  }
}
