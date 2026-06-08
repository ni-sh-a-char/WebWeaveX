/**
 * Converted from Python: core/knowledge/semantic_identity_resolver.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { identityHash } from "./semanticIdentityCalculus.js";

export function resolveSemanticIdentities(entities: any, namespace: any = ""): any {
  var resolved: any = py.iter(py.or2(entities, () => ([]))).filter((e: any) => py.truthy(e)).map((e: any) => identityHash(e, namespace));
  var by_id: any = Object.fromEntries(py.iter(resolved).map((r: any) => ([py.at(r, "id"), py.at(r, "name")] as [any, any])));
  return {"entities": resolved, "index": by_id, "count": py.len(resolved)};
}
export { identityHash };
