/**
 * Converted from Python: core/distributed_extraction/distributed_stream_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { mergeStreamRuntimes } from "../streaming/streamPersistenceEngine.js";

export function federateStreamRuntimes(streams: any): any {
  var payloads: any[] = [];
  var index: any;
  var stream: any;
  for ([index, stream] of py.enumerate(streams)) {
    var events: any = py.get(stream, "events", []);
    if ((!py.truthy(events) && py.truthy(py.get(stream, "stream_runtime")))) {
      events = py.get(py.at(stream, "stream_runtime"), "events", []);
    }
    py.listAppend(payloads, {"source": py.toStr(py.get(stream, "worker_id", `worker_${py.toStr(index)}`)), "events": [...py.iter(events)]});
  }
  var merged: any = mergeStreamRuntimes(payloads);
  return {"events": py.get(merged, "events", []), "stream_count": py.get(merged, "stream_count", 0), "bounded": true};
}
export { mergeStreamRuntimes };
