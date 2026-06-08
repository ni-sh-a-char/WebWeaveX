/**
 * Converted from Python: core/evidence/incompleteness_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelIncompleteness } from "./semanticIncompletenessEngine.js";

export function preserveIncompleteness(bundle: any): any {
  var known: any = {"observed": py.get(bundle, "observed", {}), "parsed": py.get(bundle, "parsed", {}), "reconciled": py.get(bundle, "reconciled", {})};
  var unknown: any[] = [];
  var unsupported: any[] = [];
  if (!py.truthy(py.get(bundle, "evidence"))) {
    py.listAppend(unsupported, "no_evidence");
  }
  if (py.truthy(py.get(bundle, "ambiguities"))) {
    py.extend(unknown, py.get(bundle, "ambiguities", []));
  }
  var contradicted: any = py.or2(py.get(bundle, "contradicted", {}), () => ({}));
  if ((py.truthy(py.get(contradicted, "preserved")) || py.truthy(py.get(contradicted, "pairs")))) {
    py.listAppend(unknown, "unresolved_contradiction");
  }
  var incomplete: any = modelIncompleteness(known, unknown, unsupported);
  return {"known": py.at(incomplete, "known"), "unknown": py.at(incomplete, "unknown"), "unsupported": py.at(incomplete, "unsupported"), "ambiguous": py.get(bundle, "ambiguities", []), "contradicted": contradicted, "incomplete": py.at(incomplete, "incomplete")};
}
export { modelIncompleteness };
