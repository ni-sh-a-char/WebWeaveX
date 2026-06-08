/**
 * Converted from Python: core/adaptive/layout_resilience_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeDomSimilarity } from "./domSimilarityEngine.js";

export function assessLayoutResilience(before_nodes: any, after_nodes: any): any {
  var similarity: any = computeDomSimilarity(before_nodes, after_nodes);
  return {"resilient": (py.get(similarity, "score", py.F(0.0)) >= py.F(0.3)), "similarity": similarity, "bounded": true};
}
export { computeDomSimilarity };
