/**
 * Converted from Python: core/documents/discourse_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructDiscourse } from "./discourseStructureEngine.js";
import { structureCognition } from "../evidence/index.js";

export function reconstructDiscourseDependencies(text: any): any {
  var discourse: any = reconstructDiscourse(text);
  var extends_: any = py.get(py.get(py.get(discourse, "inferred", {}), "discourse", {}), "extends", []);
  var introduces: any = py.get(py.get(py.get(discourse, "inferred", {}), "discourse", {}), "introduces", []);
  var observed: any = {"introduces": introduces};
  var inferred: any = {"discourse_dependencies": extends_, "introduces": introduces};
  var reconciled: any = {"discourse_flow": extends_, "introduces": introduces};
  return structureCognition(observed, inferred, reconciled, null);
}
export { reconstructDiscourse, structureCognition };
