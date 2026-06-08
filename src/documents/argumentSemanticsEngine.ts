/**
 * Converted from Python: core/documents/argument_semantics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildArgumentDependencies } from "./argumentDependencyEngine.js";
import { assignSemanticRoles } from "./semanticRoleEngine.js";

export function analyzeArgumentSemantics(text: any): any {
  var deps: any = buildArgumentDependencies(text);
  var roles: any = assignSemanticRoles(text);
  return {"dependencies": py.get(deps, "dependencies", []), "nodes": py.get(deps, "nodes", []), "roles": py.get(roles, "roles", []), "evidence": py.get(deps, "evidence", []), "structures": ["argumentative", "rhetorical"]};
}
export { assignSemanticRoles, buildArgumentDependencies };
