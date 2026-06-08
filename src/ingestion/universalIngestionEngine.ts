/**
 * Converted from Python: core/ingestion/universal_ingestion_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractMultimodal } from "../multimodal/universalMultimodalExtractionEngine.js";

export let SUPPORTED_EXTENSIONS: any = {".pdf": "pdf", ".docx": "docx", ".pptx": "pptx", ".xlsx": "xlsx", ".csv": "csv", ".json": "json", ".xml": "xml", ".html": "html", ".md": "markdown", ".txt": "text", ".py": "repository", ".js": "repository", ".ts": "repository", ".zip": "archive", ".png": "image", ".jpg": "image", ".jpeg": "image"};
export function detectInputType(path: any): any {
  if ((py.truthy(py.startswith(path, "http://")) || py.truthy(py.startswith(path, "https://")))) {
    return "url";
  }
  var ext: any = String(py.path(path).suffix).toLowerCase();
  return py.get(SUPPORTED_EXTENSIONS, ext, "unknown");
}
export function ingestInput(path: any): any {
  var input_type: any = detectInputType(path);
  if (py.eq(input_type, "image")) {
    var multimodal: any = extractMultimodal(path);
    return {"path": path, "type": "image", "input_type": input_type, "supported": true, "multimodal": multimodal, "bounded": true};
  }
  return {"path": path, "input_type": input_type, "supported": !py.eq(input_type, "unknown"), "bounded": true};
}
export { extractMultimodal };
