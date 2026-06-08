/**
 * Converted from Python: core/documents/reconstruction/api_contract_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractApiContracts(text: any): any {
  var src: any = py.or2(text, () => (""));
  var endpoints: any = py.sorted(py.toSet(py.reFindall("`(GET|POST|PUT|DELETE|PATCH)\\s+([^`]+)`", src, "")));
  var graphql: any = py.truthy(py.or2(py.contains(src, "type Query"), () => (py.contains(src, "schema {"))));
  return {"routes": py.iter(endpoints).map(([m, p]: any) => ({"method": m, "path": p})), "graphql": graphql};
}
