/**
 * Converted from Python: core/ocr/ocr_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

var pytesseract: any = null;
var Image: any = null;
pytesseract = null;
Image = null;
export let MAX_IMAGE_DIMENSION: any = 5000;
export let MAX_OCR_REGIONS: any = 10000;
export let MAX_REGION_TEXT: any = 10000;
export function extractOcr(path: any): any {
  if (((pytesseract === null || pytesseract === undefined) || (Image === null || Image === undefined))) {
    return {"available": false, "regions": [], "reason": "ocr_dependencies_missing", "bounded": true};
  }
  if (!py.truthy(py.path(path).is_file())) {
    return {"available": false, "regions": [], "reason": "file_not_found", "bounded": true};
  }
  try {
    var image: any = Image.open(path);
  } catch (exc: any) {
    return {"available": false, "regions": [], "reason": py.slice(py.toStr(exc), null, 200), "bounded": true};
  }
  const _d1 = py.iter(image.size) as any[];
  var width: any = _d1[0];
  var height: any = _d1[1];
  if ((py.gt(width, MAX_IMAGE_DIMENSION) || py.gt(height, MAX_IMAGE_DIMENSION))) {
    return {"available": false, "regions": [], "reason": "image_too_large", "bounded": true};
  }
  var regions: any[] = [];
  try {
    var data: any = pytesseract.image_to_data(image, pytesseract.Output.DICT);
    var count: any = py.len(py.get(data, "text", []));
    var idx: any;
    for (idx = 0; idx < py.min([count, MAX_OCR_REGIONS]); idx++) {
      var text: any = py.strip(py.toStr(py.at(py.at(data, "text"), idx)));
      if (!py.truthy(text)) {
        continue;
      }
      py.listAppend(regions, {"bbox": [py.toInt(py.at(py.at(data, "left"), idx)), py.toInt(py.at(py.at(data, "top"), idx)), py.toInt(py.at(py.at(data, "width"), idx)), py.toInt(py.at(py.at(data, "height"), idx))], "text": py.slice(text, null, MAX_REGION_TEXT)});
    }
  } catch (_e: any) {
    var text_result: any = extractOcrText(path);
    if (!py.truthy(py.get(text_result, "available"))) {
      return {"available": false, "regions": [], "reason": py.get(text_result, "reason", "ocr_failed"), "bounded": true};
    }
    var line_idx: any;
    var line: any;
    for ([line_idx, line] of py.enumerate(py.slice(py.splitlines(py.get(text_result, "text", "")), null, MAX_OCR_REGIONS))) {
      line = py.strip(line);
      if (!py.truthy(line)) {
        continue;
      }
      py.listAppend(regions, {"bbox": [0, py.mul(line_idx, 20), width, 20], "text": py.slice(line, null, MAX_REGION_TEXT)});
    }
  }
  return {"available": true, "regions": py.slice(regions, null, MAX_OCR_REGIONS), "bounded": true};
}
export function extractOcrText(path: any): any {
  if (((pytesseract === null || pytesseract === undefined) || (Image === null || Image === undefined))) {
    return {"available": false, "reason": "ocr_dependencies_missing", "bounded": true};
  }
  if (!py.truthy(py.path(path).is_file())) {
    return {"available": false, "reason": "file_not_found", "bounded": true};
  }
  try {
    var image: any = Image.open(path);
  } catch (exc: any) {
    return {"available": false, "reason": py.slice(py.toStr(exc), null, 200), "bounded": true};
  }
  const _d2 = py.iter(image.size) as any[];
  var width: any = _d2[0];
  var height: any = _d2[1];
  if ((py.gt(width, MAX_IMAGE_DIMENSION) || py.gt(height, MAX_IMAGE_DIMENSION))) {
    return {"available": false, "reason": "image_too_large", "bounded": true};
  }
  try {
    var text: any = pytesseract.image_to_string(image);
  } catch (exc: any) {
    return {"available": false, "reason": py.slice(py.toStr(exc), null, 200), "bounded": true};
  }
  return {"available": true, "text": py.slice(text, null, 1000000), "bounded": true};
}
