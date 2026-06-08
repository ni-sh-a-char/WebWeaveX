/**
 * Converted from Python: core/repository/service_interaction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function inferServiceInteractions(parsed: any, files: any): any {
  var calls: any = py.or2(py.get(py.or2(parsed, () => ({})), "calls", {}), () => ({}));
  var call_list: any = (((calls !== null && typeof calls === "object" && !Array.isArray(calls) && !(calls instanceof Set) && !(calls instanceof Map))) ? py.get(calls, "calls", []) : []);
  var services: any = py.toSet(py.iter(files).filter((f: any) => (py.contains(f, "docker-compose") || py.contains(f, "k8s") || py.contains(f, "deployment"))).map((f: any) => f));
  var interactions: any = py.iter(py.slice(call_list, null, 100)).filter((c: any) => (((c !== null && typeof c === "object" && !Array.isArray(c) && !(c instanceof Set) && !(c instanceof Map))) && py.truthy(py.get(c, "caller")))).map((c: any) => ({"from": py.get(c, "caller", ""), "to": py.get(c, "callee", ""), "evidence": ["parser:call_graph"]}));
  return {"interactions": interactions, "service_files": py.sorted(services), "evidence": (py.truthy(interactions) ? ["parser:call_graph"] : [])};
}
