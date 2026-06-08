/**
 * Converted from Python: core/files/html_file_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractSemanticHtml } from "../browser/htmlSemanticExtractionEngine.js";
import { reconstructDom } from "../dom/domReconstructionEngine.js";
import { extractSemanticContent } from "../extraction/semanticContentExtractionEngine.js";
import { compileBrowserIr } from "../ir/browserIr.js";
import { extractDocumentRuntime } from "../documents/universalDocumentExtractionEngine.js";

export let MAX_HTML_FILE: any = 10000000;
export function extractHtmlFile(path: any): any {
  if (!py.truthy(py.path(path).is_file())) {
    return {"available": false, "reason": "file_not_found", "bounded": true};
  }
  var f: any = py.open(path, "r");
  var html: any = f.read(MAX_HTML_FILE);
  var semantic: any = extractSemanticHtml(html);
  var dom: any = reconstructDom(html);
  var extraction: any = extractSemanticContent(html);
  var browser_ir: any = compileBrowserIr({"available": true, "source": "file", "path": path, "title": py.get(semantic, "title", ""), "html": py.slice(html, null, MAX_HTML_FILE), "bounded": true}, dom, extraction, {"requests": [], "bounded": true});
  var extracted_text: any = py.get(semantic, "text", "");
  var document_runtime: any = extractDocumentRuntime(extracted_text);
  return {"available": true, "html": py.slice(html, null, MAX_HTML_FILE), "text": py.slice(extracted_text, null, 5000000), "semantic": semantic, "dom": dom, "extraction": extraction, "browser_ir": browser_ir, "document_runtime": document_runtime, "bounded": true};
}
export { compileBrowserIr, extractDocumentRuntime, extractSemanticContent, extractSemanticHtml, reconstructDom };
