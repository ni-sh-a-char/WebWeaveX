/**
 * Converted from Python: core/adaptive/extraction_fallback_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { healSelector } from "./selectorHealingEngine.js";
import { buildSemanticAnchor } from "./semanticAnchorEngine.js";

export function buildExtractionFallbackChain(primary_selector: any, dom_nodes: any, html: any = ""): any {
  var healed: any = healSelector(primary_selector, dom_nodes, html);
  var anchor: any = buildSemanticAnchor(primary_selector, html);
  var chain: any = [{"step": 0, "strategy": "primary", "selector": primary_selector}, {"step": 1, "strategy": "healed_selector", "selector": py.get(healed, "healed_selector", primary_selector)}, {"step": 2, "strategy": "semantic_anchor", "selector": (py.truthy(py.get(anchor, "matched")) ? py.at(py.at(py.at(anchor, "matched"), 0), "text") : primary_selector)}, {"step": 3, "strategy": "structural_traversal", "selector": (py.truthy(dom_nodes) ? py.get(py.at(dom_nodes, 0), "tag", "div") : "div")}, {"step": 4, "strategy": "text_fallback", "selector": "body"}];
  return {"chain": chain, "active": (py.truthy(py.get(healed, "healed_selector")) ? py.at(chain, 1) : py.at(chain, 0)), "bounded": true};
}
export { buildSemanticAnchor, healSelector };
