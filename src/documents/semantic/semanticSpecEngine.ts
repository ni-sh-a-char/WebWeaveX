/**
 * Converted from Python: core/documents/semantic/semantic_spec_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractSemanticSpecs(text: any): any {
  var source: any = py.or2(text, () => (""));
  var rfc: any = py.sorted(py.toSet(py.reFindall("\\bRFC\\s*-?\\s*(\\d+)\\b", source, "i")));
  var versioned: any = py.sorted(py.toSet(py.reFindall("\\bv\\d+(?:\\.\\d+){0,2}\\b", source, "")));
  var keywords: any[] = [];
  var kw: any;
  for (kw of py.iter(["MUST", "SHOULD", "MAY", "REQUIRED", "OPTIONAL"])) {
    if (py.truthy(py.reSearch(`\\b${py.toStr(kw)}\\b`, source, ""))) {
      py.listAppend(keywords, kw);
    }
  }
  return {"rfc": rfc, "versions": versioned, "normative_keywords": py.sorted(keywords)};
}
