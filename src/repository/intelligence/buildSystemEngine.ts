/**
 * Converted from Python: core/repository/intelligence/build_system_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function detectBuildSystems(text: any): any {
  var src: any = String(py.or2(text, () => (""))).toLowerCase();
  var out: any[] = [];
  var k: any;
  var v: any;
  for ([k, v] of py.iter([["pyproject.toml", "python"], ["package.json", "node"], ["pom.xml", "maven"], ["build.gradle", "gradle"], ["cargo.toml", "cargo"]])) {
    if (py.contains(src, k)) {
      py.listAppend(out, v);
    }
  }
  return py.sorted(py.toSet(out));
}
