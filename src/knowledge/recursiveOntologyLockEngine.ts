/**
 * Converted from Python: core/knowledge/recursive_ontology_lock_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { _closureRecord } from "../evidence/recursiveSemanticClosureEngine.js";

export function suppressRecursiveOntologyLock(edge: any, depth: any = 0): any {
  var ev: any = py.or2(py.get(edge, "evidence", []), () => ([]));
  var lock: any = py.and2((depth >= 2), () => ((py.len(ev) < 2)));
  var record: any = (py.truthy(lock) ? _closureRecord("recursive_ontology_lock", depth) : null);
  return {...(edge), "recursive_reality_integrity": {"preserved": !py.truthy(lock), "lock_suppressed": lock}, "recursive_entropy": py.get(edge, "entropy", {"level": (py.truthy(lock) ? py.F(0.3) : py.F(0.1))}), "recursive_instability": {"unstable": lock, "preserved": true}, "recursive_truth_boundaries": {"lock_in_allowed": false}, "recursive_decay": {"active": lock}, "recursive_contradictions": py.get(edge, "contradictions", {"preserved": true}), "recursive_closure_suppressed": record};
}
