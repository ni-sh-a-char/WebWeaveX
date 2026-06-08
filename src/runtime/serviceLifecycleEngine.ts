/**
 * Converted from Python: core/runtime/service_lifecycle_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let LIFECYCLE_PHASES: any = ["bootstrap", "ready", "serving", "draining", "stopped"];
export function inferServiceLifecycle(services: any, parser_evidence: any): any {
  var phases: any[] = [];
  var svc: any;
  for (svc of py.iter(py.sorted(services, {key: ((s: any) => py.toStr(py.get(s, "name", ""))) as (item: any) => any}))) {
    var phase: any = String(py.toStr(py.get(svc, "phase", "bootstrap"))).toLowerCase();
    if (!py.contains(LIFECYCLE_PHASES, phase)) {
      phase = "bootstrap";
    }
    py.listAppend(phases, {"name": py.get(svc, "name"), "phase": phase});
  }
  return {"services": phases, "evidence": py.sorted(py.toSet(parser_evidence)), "grounded": py.truthy(parser_evidence), "deterministic": true};
}
