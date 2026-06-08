/**
 * Converted from Python: core/evidence/recursive_centralization_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectRecursiveCentralization(decentralized: any, depth: any): any {
  var centralized: any = py.and2(!py.truthy(decentralized), () => ((depth >= 2)));
  return {"centralized": centralized, "suppress": centralized};
}
