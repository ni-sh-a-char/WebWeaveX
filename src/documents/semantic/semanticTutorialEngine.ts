/**
 * Converted from Python: core/documents/semantic/semantic_tutorial_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractSemanticTutorials(text: any): any {
  var source: any = py.or2(text, () => (""));
  var headings: any = py.reFindall("^(#+)\\s+(.+)$", source, "m");
  var steps: any[] = [];
  var hashes: any;
  var title: any;
  for ([hashes, title] of py.iter(headings)) {
    if ((py.len(hashes) <= 3)) {
      py.listAppend(steps, py.strip(title));
    }
  }
  var ordered: any = py.sorted(py.toSet(py.reFindall("^\\s*\\d+\\.\\s+(.+)$", source, "m")));
  return {"steps": py.sorted(py.toSet(steps)), "ordered_items": ordered};
}
