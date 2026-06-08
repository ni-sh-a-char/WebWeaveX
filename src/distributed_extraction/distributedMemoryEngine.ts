/**
 * Converted from Python: core/distributed_extraction/distributed_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function mergeDistributedMemory(memories: any): any {
  var merged: any = {"workers": [], "adaptive": {}, "streams": [], "bounded": true};
  var memory: any;
  for (memory of py.iter(memories)) {
    py.listAppend(py.at(merged, "workers"), py.get(memory, "worker_id", ""));
    py.update(py.at(merged, "adaptive"), py.get(memory, "adaptive", {}));
    py.extend(py.at(merged, "streams"), py.get(memory, "streams", []));
  }
  return merged;
}
