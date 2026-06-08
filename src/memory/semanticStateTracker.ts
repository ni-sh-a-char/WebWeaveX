/**
 * Converted from Python: core/memory/semantic_state_tracker.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { SemanticMemory } from "./semanticMemoryEngine.js";

export class SemanticStateTracker {
  declare memory: any;
  declare version: any;
  constructor(max_entries: any = 128) {
    this.memory = new SemanticMemory(max_entries);
    this.version = 0;
  }
  commit(key: any, state: any): any {
    this.version = py.add(this.version, 1);
    var wrapped: any = {...(state), "version": this.version, "lineage": {"stage": "commit", "version": this.version}};
    this.memory.put(key, wrapped, py.get(wrapped, "lineage"));
    return wrapped;
  }
  current(key: any): any {
    return py.or2(py.get(this.memory, key), () => ({}));
  }
}
export { SemanticMemory };
