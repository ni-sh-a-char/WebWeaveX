/**
 * Converted from Python: core/universal/graphql_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function parseGraphql(text: any): any {
  var src: any = py.or2(text, () => (""));
  var types: any = py.sorted(py.toSet(py.reFindall("\\btype\\s+([A-Za-z_][A-Za-z0-9_]*)\\b", src, "")));
  var queries: any = py.sorted(py.toSet(py.reFindall("\\bquery\\s+([A-Za-z_][A-Za-z0-9_]*)\\b", src, "")));
  return {"types": types, "queries": queries};
}
