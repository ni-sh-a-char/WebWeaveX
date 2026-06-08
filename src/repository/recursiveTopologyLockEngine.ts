/**
 * Converted from Python: core/repository/recursive_topology_lock_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { _closureRecord } from "../evidence/recursiveSemanticClosureEngine.js";

export function suppressRecursiveTopologyLock(edge: any, depth: any = 0): any {
  var ev: any = py.or2(py.get(edge, "evidence", []), () => ([]));
  var lock: any = py.and2((depth >= 2), () => (!py.truthy(ev)));
  var record: any = (py.truthy(lock) ? _closureRecord("recursive_topology_lock", depth) : null);
  return {...(edge), "recursive_reality_integrity": {"preserved": !py.truthy(lock), "lock_suppressed": lock}, "recursive_entropy": py.get(edge, "entropy", {"level": (py.truthy(lock) ? py.F(0.4) : py.F(0.1))}), "recursive_instability": {"unstable": py.or2(lock, () => (!py.truthy(ev))), "preserved": true}, "recursive_truth_boundaries": {"normalization_allowed": false}, "recursive_decay": {"active": lock}, "recursive_uncertainty": py.get(edge, "uncertainty", {"visible": !py.truthy(ev)}), "recursive_ambiguity": py.get(edge, "ambiguity", {"visible": false}), "recursive_contradictions": {"preserved": true}, "recursive_closure_suppressed": record};
}
