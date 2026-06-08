/**
 * Converted from Python: core/documents/recursive/versioned_docs_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function detectVersions(text: any): any {
  var versions: any = py.sorted(py.toSet(py.reFindall("\\b(v?\\d+\\.\\d+(?:\\.\\d+)?)\\b", py.or2(text, () => ("")), "")));
  return {"versions": versions};
}
