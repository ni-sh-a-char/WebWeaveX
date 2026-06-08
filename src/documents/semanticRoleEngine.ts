/**
 * Converted from Python: core/documents/semantic_role_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _ROLE_PATTERNS: any = [[py.regex("\\b(example|for instance)\\b", "i"), "example"], [py.regex("\\b(therefore|thus|hence)\\b", "i"), "conclusion"], [py.regex("\\b(because|since|due to)\\b", "i"), "reason"], [py.regex("\\b(note|warning|caution)\\b", "i"), "notice"]];
export function assignSemanticRoles(text: any): any {
  var roles: any[] = [];
  var i: any;
  var ln: any;
  for ([i, ln] of py.enumerate(py.splitlines(py.or2(text, () => (""))))) {
    var pat: any;
    var role: any;
    for ([pat, role] of py.iter(_ROLE_PATTERNS)) {
      if (py.truthy(pat.search(ln))) {
        py.listAppend(roles, {"line": i, "role": role, "text": py.slice(ln, null, 120)});
        break;
      }
    }
  }
  return {"roles": roles, "count": py.len(roles)};
}
