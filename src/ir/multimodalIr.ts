/**
 * Converted from Python: core/ir/multimodal_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function compileMultimodalIr(layout: any, tables: any, forms: any, charts: any, ui: any): any {
  var blocks: any = py.get(layout, "blocks", []);
  return {"ir": "multimodal", "semantic_blocks": blocks, "layout_tree": layout, "tables": tables, "charts": charts, "forms": forms, "navigation": [], "ui_components": ui, "layout": layout, "bounded": true};
}
