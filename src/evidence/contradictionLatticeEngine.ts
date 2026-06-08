/**
 * Converted from Python: core/evidence/contradiction_lattice_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildContradictionLattice(pairs: any): any {
  var normalized: any[] = [];
  var p: any;
  for (p of py.iter(py.or2(pairs, () => ([])))) {
    if (((Array.isArray(p) || Array.isArray(p)) && (py.len(p) >= 2))) {
      py.listAppend(normalized, [py.toStr(py.at(p, 0)), py.toStr(py.at(p, 1))]);
    }
  }
  var count: any = py.len(normalized);
  var pressure: any = py.round(py.min([py.F(1.0), py.mul(count, py.F(0.25))]), 3);
  return {"pairs": py.iter(py.sorted(normalized)).map((t: any) => [...py.iter(t)]), "count": count, "pressure": pressure, "rigor": "lattice_enumeration", "deterministic_inputs": [`pair_count=${py.toStr(count)}`, `pressure=${py.floatStr(pressure)}`]};
}
