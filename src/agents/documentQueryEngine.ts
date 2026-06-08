/**
 * Converted from Python: core/agents/document_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function queryDocument(result: any, key: any = ""): any {
  var docs: any = py.get(py.get(result, "content", {}), "documents", {});
  return (!py.truthy(key) ? docs : py.get(docs, key));
}
