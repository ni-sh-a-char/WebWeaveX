/**
 * Converted from Python: core/documents/entity_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractReferences } from "./referenceEngine.js";

export function resolveReferences(text: any): any {
  var refs: any = extractReferences(py.or2(text, () => ("")));
  var external: any = py.get(refs, "external_links", py.get(refs, "external", []));
  var internal: any = py.get(refs, "internal_links", py.get(refs, "internal", []));
  var anchors: any = py.sorted(py.toSet(py.reFindall("\\[[^\\]]+\\]\\((#[^)]+)\\)", py.or2(text, () => ("")), "")));
  return {"external": external, "internal": internal, "anchors": anchors, "evidence": "reference_engine"};
}
export { extractReferences };
