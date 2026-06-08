/**
 * Converted from Python: core/dom/dom_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_DOM_NODES: any = 100000;
export function reconstructDom(html: any): any {
  var soup: any = py.soup(html, "html.parser");
  var nodes: any[] = [];
  var count: any = 0;
  var tag: any;
  for (tag of py.iter(soup.find_all())) {
    if (py.ge(count, MAX_DOM_NODES)) {
      break;
    }
    py.listAppend(nodes, {"tag": tag.name, "text": py.slice(tag.get_text(true), null, 500)});
    count = py.add(count, 1);
  }
  return {"nodes": nodes, "node_count": py.len(nodes), "bounded": true};
}
