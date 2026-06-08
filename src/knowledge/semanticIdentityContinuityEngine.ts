/**
 * Converted from Python: core/knowledge/semantic_identity_continuity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { resolveSemanticIdentities } from "./semanticIdentityResolver.js";

export function trackIdentityContinuity(entities_before: any, entities_after: any): any {
  var b: any = resolveSemanticIdentities(entities_before);
  var a: any = resolveSemanticIdentities(entities_after);
  var b_ids: any = py.toSet(py.iter(py.get(b, "entities", [])).map((e: any) => py.at(e, "id")));
  var a_ids: any = py.toSet(py.iter(py.get(a, "entities", [])).map((e: any) => py.at(e, "id")));
  return {"continuous": py.sorted(py.bitand(b_ids, a_ids)), "added": py.sorted(py.sub(a_ids, b_ids)), "removed": py.sorted(py.sub(b_ids, a_ids))};
}
export { resolveSemanticIdentities };
