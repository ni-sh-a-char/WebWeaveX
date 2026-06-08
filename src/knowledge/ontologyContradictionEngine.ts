/**
 * Converted from Python: core/knowledge/ontology_contradiction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildContradictionLattice } from "../evidence/contradictionLatticeEngine.js";

export function modelOntologyContradiction(edge: any): any {
  var pairs: any = py.get(py.or2(py.get(edge, "contradictions", {}), () => ({})), "pairs", []);
  var lattice: any = buildContradictionLattice(pairs);
  var pressure: any = py.at(lattice, "pressure");
  return {...(edge), "contradiction_pressure": pressure, "contradiction_lattice": lattice};
}
export { buildContradictionLattice };
