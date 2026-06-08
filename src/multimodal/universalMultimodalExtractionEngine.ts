/**
 * Converted from Python: core/multimodal/universal_multimodal_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractOcr } from "../ocr/ocrEngine.js";
import { detectLayoutBlocks } from "../layout/layoutDetectionEngine.js";
import { extractTables } from "../tables/tableExtractionEngine.js";
import { extractForms } from "../vision/formExtractionEngine.js";
import { detectCharts } from "../vision/chartDetectionEngine.js";
import { detectUiComponents } from "../vision/uiComponentDetectionEngine.js";
import { compileMultimodalIr } from "../ir/multimodalIr.js";

export function extractMultimodal(path: any): any {
  var ocr: any = extractOcr(path);
  var layout: any = detectLayoutBlocks(py.get(ocr, "regions", []));
  var tables: any = extractTables(layout);
  var forms: any = extractForms(layout);
  var charts: any = detectCharts(layout);
  var ui: any = detectUiComponents(layout);
  var multimodal_ir: any = compileMultimodalIr(layout, tables, forms, charts, ui);
  return {"ocr": ocr, "layout": layout, "tables": tables, "forms": forms, "charts": charts, "ui": ui, "multimodal_ir": multimodal_ir, "bounded": true};
}
export { compileMultimodalIr, detectCharts, detectLayoutBlocks, detectUiComponents, extractForms, extractOcr, extractTables };
