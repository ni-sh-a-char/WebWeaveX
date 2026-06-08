/**
 * Converted from Python: core/evidence/authority_diffusion_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function diffuseAuthority(interpretations: any): any {
  return {"diffused": !py.eq(py.len(interpretations), 1), "interpretation_count": py.len(interpretations)};
}
