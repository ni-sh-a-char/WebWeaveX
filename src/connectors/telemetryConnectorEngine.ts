/**
 * Converted from Python: core/connectors/telemetry_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractTelemetryRuntime(backends: any = null, snapshot: any = null): any {
  backends = py.or2(backends, () => (["opentelemetry", "prometheus", "jaeger"]));
  var snap: any = py.or2(snapshot, () => ({}));
  return {"backends": py.sorted(backends), "metrics": [...py.iter(py.get(snap, "metrics", []))], "traces": [...py.iter(py.get(snap, "traces", []))], "spans": py.slice([...py.iter(py.get(snap, "spans", []))], null, 10000), "logs": py.slice([...py.iter(py.get(snap, "logs", []))], null, 10000), "distributed_correlations": [...py.iter(py.get(snap, "correlations", []))], "degraded": py.get(snap, "degraded", false), "bounded": true};
}
