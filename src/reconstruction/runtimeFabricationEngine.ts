/**
 * Converted from Python: core/reconstruction/runtime_fabrication_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructRuntime } from "./runtimeReconstructionEngine.js";

export function fabricateRuntimeReality(runtime: any = null, environment: any = null, browser: any = null, application: any = null, portable: any = true): any {
  var base: any = py.or2(runtime, () => (reconstructRuntime(undefined, undefined, undefined, undefined, undefined, undefined, py.toStr((py.truthy(environment) ? py.get(environment, "runtime", "browser") : "browser")))));
  var fabricated_runtime: any = {...(base), "environment": py.pyDict(py.or2(environment, () => ({}))), "browser": py.pyDict(py.or2(browser, () => ({}))), "application": py.pyDict(py.or2(application, () => ({})))};
  return {"fabricated": true, "runtime": fabricated_runtime, "portable": portable, "replay_safe": true, "operational_twin": true, "bounded": true};
}
export { reconstructRuntime };
