/**
 * Converted from Python: core/documents/semantic_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructSemanticSections } from "./semanticSectionReconstructionEngine.js";
import { structureCognition } from "../evidence/index.js";

export function reconstructSemanticDependencies(text: any): any {
  var sections: any = reconstructSemanticSections(text);
  var deps: any = py.get(py.get(py.get(sections, "inferred", {}), "semantic", {}), "explains", []);
  var support: any = py.iter(deps).filter((d: any) => ((d !== null && typeof d === "object" && !Array.isArray(d) && !(d instanceof Set) && !(d instanceof Map)))).map((d: any) => ({"from": py.at(d, "from"), "to": py.at(d, "to"), "relation": "explains"}));
  var extends_: any = py.iter(deps).filter((d: any) => ((d !== null && typeof d === "object" && !Array.isArray(d) && !(d instanceof Set) && !(d instanceof Map)))).map((d: any) => ({"from": py.at(d, "to"), "to": py.at(d, "from"), "relation": "extends"}));
  var observed: any = {"section_count": py.len(py.get(py.get(sections, "reconciled", {}), "sections", []))};
  var inferred: any = {"dependencies": support, "extensions": extends_};
  var reconciled: any = {"semantic_dependencies": py.add(support, extends_)};
  return structureCognition(observed, inferred, reconciled, null);
}
export { reconstructSemanticSections, structureCognition };
