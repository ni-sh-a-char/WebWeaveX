/**
 * Converted from Python: core/presentation/presentation_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_SLIDES: any = 1000;
export function extractPresentationStructure(slides: any): any {
  var parsed: any[] = [];
  var idx: any;
  var slide: any;
  for ([idx, slide] of py.enumerate(py.slice(slides, null, MAX_SLIDES))) {
    py.listAppend(parsed, {"slide": idx, "title": py.get(slide, "title"), "content": py.get(slide, "content")});
  }
  return {"slides": parsed, "bounded": true};
}
