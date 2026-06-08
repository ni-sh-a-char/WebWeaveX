/**
 * Converted from Python: core/documents/semantic/semantic_api_docs_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractSemanticApiDocs(text: any): any {
  var source: any = py.or2(text, () => (""));
  var endpoints: any = py.sorted(py.toSet(py.reFindall("`(GET|POST|PUT|DELETE|PATCH)\\s+([^`]+)`", source, "")));
  var params: any = py.sorted(py.toSet(py.reFindall("\\b(?:param|query|path|body)\\s*:\\s*([A-Za-z_][A-Za-z0-9_]*)", source, "i")));
  return {"endpoints": py.iter(endpoints).map(([m, p]: any) => ({"method": m, "path": py.strip(p)})), "parameters": params};
}
