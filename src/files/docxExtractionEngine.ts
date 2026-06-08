/**
 * Converted from Python: core/files/docx_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractDocumentRuntime } from "../documents/universalDocumentExtractionEngine.js";

var Document: any = null;
Document = null;
export let MAX_PARAGRAPHS: any = 10000;
export function _withDocumentRuntime(payload: any): any {
  var text: any = py.get(payload, "text", "");
  py.setItem(payload, "document_runtime", extractDocumentRuntime(text));
  return payload;
}
export function extractDocxText(path: any): any {
  if ((Document === null || Document === undefined)) {
    return _withDocumentRuntime({"available": false, "text": "", "reason": "python_docx_missing", "bounded": true});
  }
  if (!py.truthy(py.path(path).is_file())) {
    return _withDocumentRuntime({"available": false, "text": "", "reason": "file_not_found", "bounded": true});
  }
  try {
    var document: any = Document(path);
  } catch (exc: any) {
    return _withDocumentRuntime({"available": false, "text": "", "reason": py.slice(py.toStr(exc), null, 200), "bounded": true});
  }
  var paragraphs: any[] = [];
  var para: any;
  for (para of py.iter(py.slice(document.paragraphs, null, MAX_PARAGRAPHS))) {
    var text: any = py.strip(para.text);
    if (py.truthy(text)) {
      py.listAppend(paragraphs, py.slice(text, null, 10000));
    }
  }
  return _withDocumentRuntime({"available": true, "paragraphs": paragraphs, "text": py.join("\n", paragraphs), "bounded": true});
}
export { extractDocumentRuntime };
