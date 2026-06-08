/**
 * Converted from Python: core/documents/api_documentation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractApiContractDocs(text: any): any {
  var src: any = py.or2(text, () => (""));
  var routes: any = py.sorted(py.toSet(py.reFindall("`(GET|POST|PUT|DELETE|PATCH)\\s+([^`]+)`", src, "")));
  return {"routes": py.iter(routes).map(([m, p]: any) => ({"method": m, "path": p}))};
}
