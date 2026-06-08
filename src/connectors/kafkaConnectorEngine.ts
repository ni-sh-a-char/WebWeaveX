/**
 * Converted from Python: core/connectors/kafka_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractKafkaRuntime(snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  return {"stream_type": "kafka", "topics": py.sorted(py.get(snap, "topics", []), {key: (py.toStr) as (item: any) => any}), "consumers": [...py.iter(py.get(snap, "consumers", []))], "offsets": py.pyDict(py.get(snap, "offsets", {})), "propagation_state": py.toStr(py.get(snap, "state", "stable")), "event_lineage": [...py.iter(py.get(snap, "lineage", []))], "degraded": py.get(snap, "degraded", false), "bounded": true};
}
