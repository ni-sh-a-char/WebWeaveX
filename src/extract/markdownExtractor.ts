/**
 * Converted from Python: core/extract/markdown_extractor.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractMarkdown(text: any): any {
  var src: any = py.or2(text, () => (""));
  var headers: any = py.reFindall("^(#{1,6})\\s+(.+)$", src, "m");
  var hierarchy: any = py.iter(headers).map(([h, t]: any) => ({"level": py.len(h), "title": py.strip(t)}));
  var code_blocks: any = py.reFindall("```[\\w-]*\\n(.*?)```", src, "s");
  var urls: any = py.sorted(py.toSet(py.reFindall("https?://[^\\s\\)]+", src, "")));
  return {"content": {"hierarchy": hierarchy, "urls": urls}, "code": {"blocks": py.sorted(py.iter(code_blocks).filter((b: any) => py.truthy(py.strip(b))).map((b: any) => py.strip(b)))}, "metadata": {"header_count": py.toStr(py.len(hierarchy))}};
}
