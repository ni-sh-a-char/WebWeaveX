/**
 * Converted from Python: core/ir/browser_identity_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileBrowserIdentityIr(identity: any, entropy: any, replay: any): any {
  return {"ir": "browser_identity_runtime", "identity_profile": identity, "entropy_state": entropy, "navigator_runtime": py.get(identity, "navigator", {}), "replay_metadata": replay, "fingerprint_hashes": {"identity": py.get(identity, "fingerprint_hash", ""), "entropy": py.get(entropy, "baseline_hash", "")}, "bounded": true};
}
export function browserIdentityIrToRuntimeGraph(identity_ir: any): any {
  var identity: any = py.get(identity_ir, "identity_profile", {});
  var node_id: any = py.toStr(py.get(identity, "fingerprint_hash", "browser_identity"));
  return {"ir": "browser_identity_graph", "nodes": [{"id": node_id, "type": "browser_identity", "name": py.get(identity, "profile_id", "default")}], "edges": [], "bounded": true};
}
