/**
 * Converted from Python: core/documents/citation_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_REFERENCES: any = 5000;
export let CITATION_PATTERN: any = py.regex("\\[(\\d+)\\]", "");
export function extractCitations(text: any): any {
  var citations: any[] = [];
  var matches: any = CITATION_PATTERN.findall(text);
  var match: any;
  for (match of py.iter(py.slice(matches, null, MAX_REFERENCES))) {
    py.listAppend(citations, {"citation": match});
  }
  return {"citations": citations, "bounded": true};
}
