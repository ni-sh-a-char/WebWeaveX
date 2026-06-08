/**
 * Converted from Python: core/evidence/semantic_contradiction_prover.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildContradictionLattice } from "./contradictionLatticeEngine.js";

export function proveContradictionPressure(pairs: any): any {
  var lattice: any = buildContradictionLattice(pairs);
  return {"pressure": py.at(lattice, "pressure"), "count": py.at(lattice, "count"), "proved": (py.at(lattice, "count") > 0), "lattice": lattice};
}
export { buildContradictionLattice };
