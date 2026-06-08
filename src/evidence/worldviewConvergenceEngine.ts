/**
 * Converted from Python: core/evidence/worldview_convergence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function suppressWorldviewConvergence(convergence: any, depth: any): any {
  return {"convergence": py.and2(convergence, () => ((depth >= 2))), "suppress": convergence, "lock_in_prevented": true};
}
