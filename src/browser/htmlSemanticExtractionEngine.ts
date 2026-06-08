/**
 * Converted from Python: core/browser/html_semantic_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_LINKS: any = 10000;
export function extractSemanticHtml(html: any): any {
  var soup: any = py.soup(html, "html.parser");
  var title: any = "";
  if (py.truthy(soup.title)) {
    title = py.strip(soup.title.text);
  }
  var links: any[] = [];
  var link: any;
  for (link of py.iter(py.slice(soup.find_all("a"), null, MAX_LINKS))) {
    var href: any = py.get(link, "href");
    if (py.truthy(href)) {
      py.listAppend(links, py.slice(href, null, 2000));
    }
  }
  var headings: any[] = [];
  var tag: any;
  for (tag of py.iter(["h1", "h2", "h3"])) {
    var node: any;
    for (node of py.iter(soup.find_all(tag))) {
      py.listAppend(headings, {"tag": tag, "text": py.slice(node.get_text(true), null, 5000)});
    }
  }
  return {"title": title, "links": py.sorted(py.toSet(links)), "headings": headings, "text": py.slice(soup.get_text("\n"), null, 5000000), "bounded": true};
}
