/**
 * Converted from Python: core/extract/html_extractor.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractHtml(text: any): any {
  var soup: any = py.soup(py.or2(text, () => ("")), "lxml");
  var tag: any;
  for (tag of py.iter(soup(["script", "style"]))) {
    tag.decompose();
  }
  var body: any = soup.get_text(" ", true);
  var links: any = py.sorted(py.toSet(py.iter(soup.find_all("a")).filter((a: any) => py.truthy(py.get(a, "href"))).map((a: any) => py.get(a, "href", ""))));
  var code_blocks: any = py.iter(soup.find_all(["pre", "code"])).filter((c: any) => py.truthy(c.get_text(true))).map((c: any) => c.get_text("\n", true));
  return {"content": {"text": body, "links": links}, "code": {"blocks": py.sorted(code_blocks)}, "metadata": {"title": ((py.truthy(soup.title) && py.truthy(soup.title.string)) ? py.strip(soup.title.string) : "")}};
}
