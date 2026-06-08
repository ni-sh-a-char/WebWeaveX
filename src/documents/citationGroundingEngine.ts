/**
 * Converted from Python: core/documents/citation_grounding_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { structureCognition } from "../evidence/index.js";
import { reconstructCitationLineage } from "../internet/citationLineageEngine.js";

export function groundCitations(text: any): any {
  var cites: any = reconstructCitationLineage(text);
  var observed: any = {"citations": py.get(cites, "citations", [])};
  var inferred: any = {"targets": py.iter(py.get(cites, "citations", [])).map((c: any) => py.at(c, "target"))};
  var reconciled: any = {"citation_lineage": cites, "grounded_targets": py.at(inferred, "targets")};
  return structureCognition(observed, inferred, reconciled, null);
}
export { reconstructCitationLineage, structureCognition };
