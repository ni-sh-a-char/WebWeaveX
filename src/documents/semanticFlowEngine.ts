/**
 * Converted from Python: core/documents/semantic_flow_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructDiscourseDependencies } from "./discourseDependencyEngine.js";
import { reconstructNarrative } from "./semanticNarrativeEngine.js";
import { structureCognition } from "../evidence/index.js";

export function reconstructSemanticFlow(text: any): any {
  var discourse: any = reconstructDiscourseDependencies(text);
  var narrative: any = reconstructNarrative(text);
  var flow_edges: any = py.get(py.get(discourse, "reconciled", {}), "discourse_flow", []);
  var observed: any = {"discourse_edges": py.len(flow_edges)};
  var inferred: any = {"semantic_flow": flow_edges, "narrative_flow": py.get(narrative, "narrative_flow", []), "transitions": flow_edges};
  var reconciled: any = {"flow": flow_edges, "continuity": py.get(narrative, "narrative_flow", [])};
  return structureCognition(observed, inferred, reconciled, null);
}
export { reconstructDiscourseDependencies, reconstructNarrative, structureCognition };
