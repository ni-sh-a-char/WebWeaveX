/**
 * Converted from Python: core/adaptive/selector_healing_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildSemanticAnchor } from "./semanticAnchorEngine.js";

export let MAX_CANDIDATES: any = 100;
export function healSelector(selector: any, dom_nodes: any, html: any = ""): any {
  var strategies: any[] = [];
  var anchor: any = buildSemanticAnchor(selector, html);
  if (py.truthy(py.get(anchor, "matched"))) {
    var healed: any = _anchorToSelector(py.at(py.at(anchor, "matched"), 0));
    py.listAppend(strategies, {"strategy": "semantic_anchor", "selector": healed});
  }
  var node: any;
  for (node of py.iter(py.slice(dom_nodes, null, MAX_CANDIDATES))) {
    var text: any = String(py.toStr(py.get(node, "text", ""))).toLowerCase();
    var tag: any = py.toStr(py.get(node, "tag", "div"));
    var token: any = _selectorToken(selector);
    if ((py.truthy(token) && py.contains(text, token))) {
      py.listAppend(strategies, {"strategy": "text_anchor", "selector": `${py.toStr(tag)}:has-text('${py.toStr(py.slice(py.get(node, "text", ""), null, 100))}')`});
      break;
    }
  }
  for (node of py.iter(py.slice(dom_nodes, null, MAX_CANDIDATES))) {
    var attrs: any = py.get(node, "attrs", {});
    if (((attrs !== null && typeof attrs === "object" && !Array.isArray(attrs) && !(attrs instanceof Set) && !(attrs instanceof Map)))) {
      var key: any;
      for (key of py.iter(py.sorted(py.keys(attrs)))) {
        if (py.contains(new Set(["aria-label", "data-testid", "name", "id"]), key)) {
          var value: any = py.toStr(py.at(attrs, key));
          py.listAppend(strategies, {"strategy": "attribute_anchor", "selector": `[${py.toStr(key)}='${py.toStr(py.slice(value, null, 200))}']`});
          break;
        }
      }
    }
    if (py.truthy(strategies)) {
      break;
    }
  }
  if (!py.truthy(strategies)) {
    var parent_tag: any = (py.truthy(dom_nodes) ? py.get(py.at(dom_nodes, 0), "tag", "div") : "div");
    py.listAppend(strategies, {"strategy": "structural_fallback", "selector": py.toStr(parent_tag)});
  }
  healed = py.at(strategies, 0);
  return {"original": selector, "healed_selector": py.at(healed, "selector"), "strategy": py.at(healed, "strategy"), "candidates": py.slice(strategies, null, 10), "bounded": true};
}
export function _selectorToken(selector: any): any {
  var match: any = py.reSearch("#([a-zA-Z0-9_-]+)", selector, "");
  if (py.truthy(match)) {
    return String(py.replace(py.replace(match.group(1), "-", " "), "_", " ")).toLowerCase();
  }
  match = py.reSearch("\\.([a-zA-Z0-9_-]+)", selector, "");
  if (py.truthy(match)) {
    return String(py.replace(py.replace(match.group(1), "-", " "), "_", " ")).toLowerCase();
  }
  return String(py.strip(selector)).toLowerCase();
}
export function _anchorToSelector(anchor: any): any {
  var text: any = py.toStr(py.get(anchor, "text", ""));
  var anchor_type: any = py.toStr(py.get(anchor, "type", ""));
  if (py.eq(anchor_type, "aria")) {
    return `[aria-label='${py.toStr(py.slice(text, null, 200))}']`;
  }
  return `${py.toStr(anchor_type)}:has-text('${py.toStr(py.slice(text, null, 200))}')`;
}
export { buildSemanticAnchor };
