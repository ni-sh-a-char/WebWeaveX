/**
 * Converted from Python: core/internet/evidence_conflict_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildContradictionLattice } from "../evidence/contradictionLatticeEngine.js";

export function detectEvidenceConflicts(claims: any): any {
  var pairs: any[] = [];
  var texts: any = py.iter(py.or2(claims, () => ([]))).map((c: any) => py.toStr(py.get(c, "text", py.get(c, "claim", ""))));
  var i: any;
  var a: any;
  for ([i, a] of py.enumerate(texts)) {
    var b: any;
    for (b of py.iter(py.slice(texts, py.add(i, 1), null))) {
      if ((py.truthy(a) && py.truthy(b) && !py.eq(a, b) && !py.eq(py.contains(String(a).toLowerCase(), "not "), py.contains(String(b).toLowerCase(), "not ")))) {
        py.listAppend(pairs, [py.slice(a, null, 40), py.slice(b, null, 40)]);
      }
    }
  }
  var lattice: any = buildContradictionLattice(pairs);
  return {"conflicts": py.at(lattice, "pairs"), "pressure": py.at(lattice, "pressure"), "count": py.at(lattice, "count")};
}
export { buildContradictionLattice };
