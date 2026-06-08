/**
 * Converted from Python: core/reconstruction/runtime_validation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function validateReconstructedRuntime(runtime: any = null, replay: any = null, topology: any = null, execution: any = null, mutations: any = null): any {
  runtime = py.or2(runtime, () => ({}));
  replay = py.or2(replay, () => ({}));
  topology = py.or2(topology, () => ({}));
  execution = py.or2(execution, () => ({}));
  var replay_ok: any = py.truthy(py.or2(py.get(replay, "replay_chains"), () => (py.or2(py.get(replay, "replay_package"), () => (py.get(replay, "replayed"))))));
  if (py.truthy(topology)) {
    var sync_ok: any = py.truthy(py.or2(py.get(topology, "synchronization_topology"), () => (py.get(topology, "reconstructed"))));
    var topology_ok: any = py.truthy(py.or2(py.get(topology, "runtime_graph"), () => (py.get(topology, "reconstructed"))));
  } else {
    sync_ok = true;
    topology_ok = true;
  }
  var execution_ok: any = py.truthy(py.or2(py.get(execution, "executed"), () => (py.or2(py.get(execution, "actions"), () => (py.or2(py.get(runtime, "reconstructed"), () => (py.get(runtime, "fabricated"))))))));
  var mutation_list: any = (((mutations !== null && typeof mutations === "object" && !Array.isArray(mutations) && !(mutations instanceof Set) && !(mutations instanceof Map))) ? py.get(mutations, "mutations", []) : py.or2(mutations, () => ([])));
  var mutation_ok: any = (py.truthy(mutation_list) ? py.all(py.iter(mutation_list).map((m: any) => py.or2(py.contains(m, "kind"), () => (py.contains(m, "target"))))) : true);
  var checks: any = [py.or2(replay_ok, () => (py.get(runtime, "replay_safe"))), py.or2(sync_ok, () => (topology_ok)), topology_ok, execution_ok, mutation_ok];
  var valid: any = ((py.truthy(py.get(runtime, "reconstructed")) || py.truthy(py.get(runtime, "fabricated"))) ? py.all(checks) : py.truthy(py.and2(runtime, () => (replay_ok))));
  return {"valid": valid, "integrity_score": (py.truthy(valid) ? py.F(1.0) : py.F(0.0)), "replay_integrity": replay_ok, "synchronization_integrity": sync_ok, "topology_integrity": topology_ok, "execution_integrity": execution_ok, "mutation_consistency": mutation_ok, "bounded": true};
}
