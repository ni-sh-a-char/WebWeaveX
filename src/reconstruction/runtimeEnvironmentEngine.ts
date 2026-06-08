/**
 * Converted from Python: core/reconstruction/runtime_environment_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _ENV_TYPES: any = ["browser", "terminal", "electron", "connector", "vm", "distributed"];
export function buildRuntimeEnvironment(runtime: any = "browser", connectors: any = null, workers: any = null): any {
  runtime = (py.contains(_ENV_TYPES, runtime) ? runtime : "browser");
  connectors = py.or2(connectors, () => ([]));
  workers = py.or2(workers, () => ([]));
  return {"runtime": runtime, "browser": py.eq(runtime, "browser"), "terminal": py.eq(runtime, "terminal"), "electron": py.eq(runtime, "electron"), "connector": py.eq(runtime, "connector"), "vm": py.eq(runtime, "vm"), "distributed": py.eq(runtime, "distributed"), "connectors": py.sorted(connectors, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "workers": py.sorted(workers, {key: ((item: any) => py.toStr(py.get(item, "worker_id", ""))) as (item: any) => any}), "execution_ready": true, "bounded": true};
}
