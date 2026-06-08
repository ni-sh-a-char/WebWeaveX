/**
 * Converted from Python: core/distributed_extraction/extraction_worker_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function createExtractionWorker(worker_id: any, runtime_state: any = null, identity: any = null, adaptive_runtime: any = null, stream_runtime: any = null, status: any = "idle"): any {
  return {"worker_id": py.toStr(worker_id), "runtime_state": py.pyDict(py.or2(runtime_state, () => ({}))), "identity": py.pyDict(py.or2(identity, () => ({}))), "adaptive_runtime": py.pyDict(py.or2(adaptive_runtime, () => ({}))), "stream_runtime": py.pyDict(py.or2(stream_runtime, () => ({}))), "status": py.toStr(status), "bounded": true};
}
