/**
 * Converted from Python: core/knowledge/ontology_conflict_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildContradictionLattice } from "../evidence/contradictionLatticeEngine.js";

export function detectOntologyConflicts(edges: any): any {
  var pairs: any[] = [];
  var e: any;
  for (e of py.iter(py.or2(edges, () => ([])))) {
    var c: any = py.or2(py.get(e, "contradictions", {}), () => ({}));
    var p: any;
    for (p of py.iter(py.get(c, "pairs", []))) {
      if (((Array.isArray(p) || Array.isArray(p)) && (py.len(p) >= 2))) {
        py.listAppend(pairs, [py.toStr(py.at(p, 0)), py.toStr(py.at(p, 1))]);
      }
    }
  }
  var lattice: any = buildContradictionLattice(pairs);
  return {"conflicts": py.at(lattice, "pairs"), "pressure": py.at(lattice, "pressure"), "contradiction_pressure": py.at(lattice, "pressure"), "uncertainty": {"visible": (py.at(lattice, "count") > 0)}};
}
export { buildContradictionLattice };
