/**
 * Converted from Python: core/files/pdf_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractDocumentRuntime } from "../documents/universalDocumentExtractionEngine.js";

var pypdf: any = null;
pypdf = null;
export let MAX_PAGES: any = 1000;
export function _withDocumentRuntime(payload: any): any {
  var text: any = py.get(payload, "text", "");
  py.setItem(payload, "document_runtime", extractDocumentRuntime(text));
  return payload;
}
export function extractPdfText(path: any): any {
  if ((pypdf === null || pypdf === undefined)) {
    return _withDocumentRuntime({"text": "", "pages": [], "available": false, "reason": "pypdf_not_installed", "bounded": true});
  }
  if (!py.truthy(py.path(path).is_file())) {
    return _withDocumentRuntime({"text": "", "pages": [], "available": false, "reason": "file_not_found", "bounded": true});
  }
  try {
    var reader: any = pypdf.PdfReader(path);
  } catch (exc: any) {
    return _withDocumentRuntime({"text": "", "pages": [], "available": false, "reason": py.slice(py.toStr(exc), null, 200), "bounded": true});
  }
  var pages: any[] = [];
  var index: any;
  var page: any;
  for ([index, page] of py.enumerate(py.slice(reader.pages, null, MAX_PAGES))) {
    try {
      var text: any = py.or2(page.extract_text(), () => (""));
    } catch (_e: any) {
      text = "";
    }
    py.listAppend(pages, {"page": index, "text": py.slice(text, null, 50000)});
  }
  var full_text: any = py.join("\n", py.iter(pages).map((p: any) => py.at(p, "text")));
  var extracted_text: any = py.slice(full_text, null, 5000000);
  return _withDocumentRuntime({"available": true, "page_count": py.len(pages), "pages": pages, "text": extracted_text, "bounded": true});
}
export { extractDocumentRuntime };
