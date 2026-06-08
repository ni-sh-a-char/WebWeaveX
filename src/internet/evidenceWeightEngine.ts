/**
 * Converted from Python: core/internet/evidence_weight_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { scoreAuthority } from "./authorityEngine.js";
import { computeTrust } from "./trustEngine.js";

export function weightEvidence(sources: any): any {
  var weighted: any[] = [];
  var src: any;
  for (src of py.iter(py.or2(sources, () => ([])))) {
    if (!((src !== null && typeof src === "object" && !Array.isArray(src) && !(src instanceof Set) && !(src instanceof Map)))) {
      continue;
    }
    var url: any = py.toStr(py.get(src, "url", ""));
    var authority: any = py.at(scoreAuthority(url), "authority_score");
    var trust: any = py.at(computeTrust(url), "score");
    var weight: any = py.round(py.add(py.mul(authority, py.F(0.6)), py.mul(trust, py.F(0.4))), 3);
    py.listAppend(weighted, {...(src), "evidence_weight": weight});
  }
  return py.sorted(weighted, {key: ((x: any) => [(-py.at(x, "evidence_weight")), py.toStr(py.get(x, "url", ""))]) as (item: any) => any});
}
export { computeTrust, scoreAuthority };
