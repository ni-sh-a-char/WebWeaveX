/**
 * Converted from Python: core/evidence/ontology_monopoly_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectOntologyMonopoly(entity_count: any, depth: any): any {
  var monopoly: any = py.and2((entity_count <= 1), () => ((depth >= 3)));
  return {"monopoly": monopoly, "suppress": monopoly};
}
