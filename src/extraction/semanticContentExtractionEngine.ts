/**
 * Converted from Python: core/extraction/semantic_content_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_LINKS: any = 10000;
export function extractSemanticContent(html: any): any {
  var soup: any = py.soup(html, "html.parser");
  var headings: any[] = [];
  var level: any;
  for (level of py.iter(["h1", "h2", "h3"])) {
    var node: any;
    for (node of py.iter(soup.find_all(level))) {
      py.listAppend(headings, {"level": level, "text": py.slice(node.get_text(true), null, 5000)});
    }
  }
  var paragraphs: any[] = [];
  var p: any;
  for (p of py.iter(soup.find_all("p"))) {
    var text: any = p.get_text(true);
    if (py.truthy(text)) {
      py.listAppend(paragraphs, py.slice(text, null, 10000));
    }
  }
  var links: any[] = [];
  var a: any;
  for (a of py.iter(py.slice(soup.find_all("a"), null, MAX_LINKS))) {
    var href: any = py.get(a, "href");
    if (py.truthy(href)) {
      py.listAppend(links, py.slice(href, null, 2000));
    }
  }
  return {"headings": headings, "paragraphs": paragraphs, "links": py.sorted(py.toSet(links)), "bounded": true};
}
