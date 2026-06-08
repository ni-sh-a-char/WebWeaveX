/**
 * Converted from Python: core/repository/terraform_semantic_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let RESOURCE_RE: any = py.regex("resource\\s+\"([^\"]+)\"\\s+\"([^\"]+)\"", "");
export function parseTerraformSemantics(text: any): any {
  var resources: any[] = [];
  var match: any;
  for (match of py.iter(RESOURCE_RE.finditer(text))) {
    py.listAppend(resources, {"resource_type": match.group(1), "resource_name": match.group(2)});
  }
  return {"resources": resources, "count": py.len(resources), "grounded": true};
}
