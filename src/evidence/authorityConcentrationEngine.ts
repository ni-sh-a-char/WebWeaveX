/**
 * Converted from Python: core/evidence/authority_concentration_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectAuthorityConcentration(dominant: any, depth: any): any {
  var concentrated: any = py.and2(dominant, () => ((depth >= 2)));
  return {"concentrated": concentrated, "suppress": concentrated, "diffusion_required": concentrated};
}
