/**
 * Converted from Python: core/crawling/advanced/sitemap_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function parseSitemap(xml_text: any, max_urls: any = 5000): any {
  var urls: any = py.sorted(py.toSet(py.reFindall("<loc>\\s*(.*?)\\s*</loc>", py.or2(xml_text, () => ("")), "i")));
  return {"urls": py.slice(urls, null, max_urls)};
}
