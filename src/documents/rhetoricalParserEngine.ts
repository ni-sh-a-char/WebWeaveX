/**
 * Converted from Python: core/documents/rhetorical_parser_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractRhetoricalStructure } from "./rhetoricalStructureEngine.js";
import { assignSemanticRoles } from "./semanticRoleEngine.js";

export function parseRhetoricalStructure(text: any): any {
  var structure: any = extractRhetoricalStructure(text);
  var roles: any = assignSemanticRoles(text);
  var units: any = py.get(structure, "units", []);
  var role_map: any = Object.fromEntries(py.iter(py.get(roles, "roles", [])).filter((r: any) => py.contains(r, "line")).map((r: any) => ([py.at(r, "line"), py.at(r, "role")] as [any, any])));
  var enriched: any[] = [];
  var u: any;
  for (u of py.iter(units)) {
    py.listAppend(enriched, {...(u), "role": py.get(role_map, py.get(u, "line"), (py.eq(py.get(u, "type"), "heading") ? "nucleus" : "span"))});
  }
  return {"units": enriched, "unit_count": py.len(enriched), "roles": py.get(roles, "roles", []), "rhetorical_roles": py.sorted(py.toSet(py.iter(enriched).filter((r: any) => py.truthy(py.get(r, "role"))).map((r: any) => py.get(r, "role", "")))), "deterministic_inputs": py.add(py.get(structure, "deterministic_inputs", []), [`roles=${py.toStr(py.len(py.get(roles, "roles", [])))}`])};
}
export { assignSemanticRoles, extractRhetoricalStructure };
