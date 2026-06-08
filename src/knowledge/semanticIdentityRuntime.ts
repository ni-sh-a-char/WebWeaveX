/**
 * Converted from Python: core/knowledge/semantic_identity_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import { resolveSemanticIdentities } from "./semanticIdentityResolver.js";

export function resolveIdentitiesRuntime(entities: any, namespace: any = ""): any {
  return resolveSemanticIdentities(entities, namespace);
}
export { resolveSemanticIdentities };
