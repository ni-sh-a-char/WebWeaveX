/**
 * Converted from Python: core/evidence/epistemic_openness_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelEpistemicOpenness(plurality: any, decentralization: any): any {
  return {"open": py.and2(py.get(plurality, "preserved", true), () => (py.get(decentralization, "decentralized", true))), "anti_closure": true, "anti_dogmatism": true, "anti_canonicalization": true, "interpretive_openness": true};
}
