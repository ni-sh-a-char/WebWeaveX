/**
 * Converted from Python: core/fetch/pdf_fetcher.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
// from pypdf import ... (unmapped)
import { FetchResponse } from "./base.js";

throw py.err("ModuleNotFoundError", "No module named 'pypdf'");
var PdfReader: any;
export function fetchPdfSync(url: any, timeout: any = py.F(15.0)): any {
  try {
    var res: any = py.requestsGet(url, {"timeout": timeout});
    res.raise_for_status();
    var reader: any = PdfReader(py.bytesIO(res.content));
    var text: any = py.join("\n", py.iter(reader.pages).map((page: any) => py.or2(page.extract_text(), () => (""))));
    return new FetchResponse("pdf", url, res.status_code, "application/pdf", text, true, "", {"pages": py.toStr(py.len(reader.pages))}).to_dict();
  } catch (exc: any) {
    return new FetchResponse("pdf", url, 0, "application/pdf", "", false, py.toStr(exc), {}).to_dict();
  }
}
export { FetchResponse };
