/**
 * Converted from Python: core/extract/metadata_extractor.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractMetadata(text: any, source_url: any = ""): any {
  var src: any = py.or2(text, () => (""));
  return {"source_url": py.or2(source_url, () => ("")), "raw_length": py.len(src), "line_count": py.len(py.splitlines(src)), "url_count": py.len(py.toSet(py.reFindall("https?://[^\\s\\)]+", src, ""))), "content_hash": py.hashNew("sha256", py.encode(src, "utf-8")).hexdigest()};
}
