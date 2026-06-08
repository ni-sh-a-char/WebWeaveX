/**
 * Converted from Python: core/documents/coreference_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resolveCoreferences(text: any): any {
  var headings: any = py.reFindall("^#{1,6}\\s+(.+)$", py.or2(text, () => ("")), "m");
  var pronouns: any = py.reFindall("\\b(it|this|that|they|these|those)\\b", py.or2(text, () => ("")), "i");
  var antecedent: any = (py.truthy(headings) ? py.at(headings, (-1)) : "");
  var chains: any = py.iter(py.slice(pronouns, null, 50)).map((p: any) => ({"pronoun": p, "antecedent": antecedent}));
  return {"chains": chains, "count": py.len(chains)};
}
