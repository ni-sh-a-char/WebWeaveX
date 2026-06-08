/**
 * Converted from Python: core/evidence/recursive_novelty_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelRecursiveNovelty(depth: any, key_count: any, ambiguity_count: any): any {
  var novelty: any = py.round(py.min([py.F(1.0), py.add(py.add(py.mul(key_count, py.F(0.12)), py.mul(ambiguity_count, py.F(0.08))), py.mul(py.max([0, py.sub(3, depth)]), py.F(0.05)))]), 3);
  return {"novelty": novelty, "preserved": (novelty > py.F(0.1)), "exhaustion_blocked": true};
}
