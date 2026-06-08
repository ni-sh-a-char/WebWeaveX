/**
 * Converted from Python: core/adaptive/semantic_anchor_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_ANCHORS: any = 200;
export function buildSemanticAnchor(selector: any, html: any): any {
  var soup: any = py.soup(py.or2(html, () => ("")), "html.parser");
  var anchors: any[] = [];
  var heading: any;
  for (heading of py.iter(py.slice(soup.find_all(["h1", "h2", "h3", "label"]), null, MAX_ANCHORS))) {
    var text: any = heading.get_text(true);
    if (py.truthy(text)) {
      py.listAppend(anchors, {"type": heading.name, "text": py.slice(text, null, 500)});
    }
  }
  var node: any;
  for (node of py.iter(py.slice(soup.find_all(true), null, MAX_ANCHORS))) {
    var aria: any = py.get(node, "aria-label");
    if (py.truthy(aria)) {
      py.listAppend(anchors, {"type": "aria", "text": py.slice(py.toStr(aria), null, 500)});
    }
  }
  var token: any = _selectorToken(selector);
  var matched: any = py.iter(anchors).filter((anchor: any) => (py.truthy(token) && py.contains(String(py.get(anchor, "text", "")).toLowerCase(), token))).map((anchor: any) => anchor);
  return {"selector": selector, "anchors": py.sorted(anchors, {key: ((item: any) => [py.at(item, "type"), py.at(item, "text")]) as (item: any) => any}), "matched": py.slice(matched, null, 20), "bounded": true};
}
export function _selectorToken(selector: any): any {
  var match: any = py.reSearch("#([a-zA-Z0-9_-]+)", selector, "");
  if (py.truthy(match)) {
    return String(py.replace(match.group(1), "-", " ")).toLowerCase();
  }
  match = py.reSearch("\\.([a-zA-Z0-9_-]+)", selector, "");
  if (py.truthy(match)) {
    return String(py.replace(match.group(1), "-", " ")).toLowerCase();
  }
  return String(py.strip(selector)).toLowerCase();
}
