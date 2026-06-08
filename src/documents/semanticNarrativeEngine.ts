/**
 * Converted from Python: core/documents/semantic_narrative_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructDiscourse } from "./discourseStructureEngine.js";
import { structureCognition } from "../evidence/index.js";

export function reconstructNarrative(text: any): any {
  var discourse: any = reconstructDiscourse(text);
  var flow: any = py.get(py.get(py.get(discourse, "reconciled", {}), "structure", {}), "extends", []);
  var observed: any = {"discourse": py.get(discourse, "observed", {})};
  var inferred: any = {"narrative_flow": flow};
  var reconciled: any = {"explains": flow, "depends_on": []};
  var out: any = structureCognition(observed, inferred, reconciled, null);
  py.setItem(out, "narrative_flow", flow);
  return out;
}
export { reconstructDiscourse, structureCognition };
