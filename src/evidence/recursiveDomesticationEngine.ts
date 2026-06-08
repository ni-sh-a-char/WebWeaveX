/**
 * Converted from Python: core/evidence/recursive_domestication_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectRecursiveDomestication(passive: any, depth: any): any {
  var domesticated: any = py.and2(passive, () => ((depth >= 3)));
  return {"domesticated": domesticated, "suppress": domesticated};
}
