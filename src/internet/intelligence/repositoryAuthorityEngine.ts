/**
 * Converted from Python: core/internet/intelligence/repository_authority_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function scoreRepositoryAuthority(url: any, stars: any = 0, forks: any = 0): any {
  var u: any = String(py.or2(url, () => (""))).toLowerCase();
  var base: any = py.F(0.2);
  if (py.contains(u, "github.com")) {
    base = py.add(base, py.F(0.2));
  }
  var score: any = py.add(py.add(base, py.min([py.F(0.3), py.div(stars, py.F(100000.0))])), py.min([py.F(0.3), py.div(forks, py.F(50000.0))]));
  return {"score": py.round(py.min([py.F(1.0), score]), 6)};
}
