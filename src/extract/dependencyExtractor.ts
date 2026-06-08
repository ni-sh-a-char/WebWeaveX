/**
 * Converted from Python: core/extract/dependency_extractor.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractDependencies(text: any): any {
  var src: any = py.or2(text, () => (""));
  var deps: any = py.sorted(py.toSet(py.reFindall("(?:pip install|npm i|npm install)\\s+([A-Za-z0-9_\\-\\.@/]+)", src, "")));
  try {
    var data: any = py.jsonLoads(src);
  } catch (_e: any) {
    data = {};
  }
  if (((data !== null && typeof data === "object" && !Array.isArray(data) && !(data instanceof Set) && !(data instanceof Map)))) {
    var key: any;
    for (key of py.iter(["dependencies", "devDependencies", "peerDependencies"])) {
      var section: any = py.get(data, key, {});
      if (((section !== null && typeof section === "object" && !Array.isArray(section) && !(section instanceof Set) && !(section instanceof Map)))) {
        py.extend(deps, py.keys(section));
      }
    }
  }
  return {"packages": py.sorted(py.toSet(deps))};
}
