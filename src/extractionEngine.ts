/**
 * Converted from Python: core/extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";

export function _removeScripts(html: any): any {
  return py.reSub("<script.*?>.*?</script>", "", html, 0, "si");
}
export function _removeStyles(html: any): any {
  return py.reSub("<style.*?>.*?</style>", "", html, 0, "si");
}
export function _removeComments(html: any): any {
  return py.reSub("<!--.*?-->", "", html, 0, "s");
}
export function _stripTags(html: any): any {
  return py.reSub("<[^>]+>", " ", html, 0, "");
}
export function _normalizeWhitespace(text: any): any {
  return py.strip(py.reSub("\\s+", " ", text, 0, ""));
}
export function extractText(html: any): any {
  if (!py.truthy(html)) {
    return "";
  }
  html = _removeScripts(html);
  html = _removeStyles(html);
  html = _removeComments(html);
  var text: any = _stripTags(html);
  text = _normalizeWhitespace(text);
  return text;
}
export function _extractPreBlocks(html: any): any {
  var blocks: any = py.reFindall("<pre.*?>(.*?)</pre>", html, "si");
  return py.iter(blocks).filter((b: any) => py.truthy(py.strip(b))).map((b: any) => py.strip(b));
}
export function _extractCodeBlocks(html: any): any {
  var blocks: any = py.reFindall("<code.*?>(.*?)</code>", html, "si");
  return py.iter(blocks).filter((b: any) => py.truthy(py.strip(b))).map((b: any) => py.strip(b));
}
export function extractCode(html: any): any {
  if (!py.truthy(html)) {
    return [];
  }
  var code_blocks: any[] = [];
  var pre_blocks: any = _extractPreBlocks(html);
  var code_blocks_raw: any = _extractCodeBlocks(html);
  var all_blocks: any = py.add(pre_blocks, code_blocks_raw);
  var idx: any;
  var block: any;
  for ([idx, block] of py.enumerate(all_blocks)) {
    py.listAppend(code_blocks, {"id": idx, "content": block, "length": py.len(block)});
  }
  return code_blocks;
}
export function extractContent(html: any): any {
  if (!(typeof html === "string")) {
    throw py.err("TypeError", "html must be a string");
  }
  if (py.eq(py.strip(html), "")) {
    return {"text": "", "code": [], "metadata": {"empty": true}};
  }
  var text: any = extractText(html);
  var code: any = extractCode(html);
  return {"text": text, "code": code, "metadata": {"text_length": py.len(text), "code_blocks": py.len(code)}};
}
export function validateExtractionEngine(): any {
  var test_html: any = "\n    <html>\n        <body>\n            <h1>Hello World</h1>\n            <pre>def test(): return 1</pre>\n            <script>var x = 1;</script>\n        </body>\n    </html>\n    ";
  var result: any = extractContent(test_html);
  if (!((result !== null && typeof result === "object" && !Array.isArray(result) && !(result instanceof Set) && !(result instanceof Map)))) {
    throw py.err("RuntimeError", "Result is not dict");
  }
  if (!py.contains(result, "text")) {
    throw py.err("RuntimeError", "Missing text");
  }
  if (!py.contains(result, "code")) {
    throw py.err("RuntimeError", "Missing code");
  }
  if (py.eq(py.len(py.at(result, "code")), 0)) {
    throw py.err("RuntimeError", "Code extraction failed");
  }
  if (py.contains(String(py.at(result, "text")).toLowerCase(), "script")) {
    throw py.err("RuntimeError", "Script not removed");
  }
  return true;
}
export class BaseExtractor {
  static priority = 0;
  can_handle(url: any, html: any, metadata: any): any {
    return false;
  }
  extract(url: any, html: any, metadata: any): any {
    throw py.err("NotImplementedError");
  }
}
(BaseExtractor.prototype as Record<string, any>)["priority"] = (BaseExtractor as Record<string, any>)["priority"];
