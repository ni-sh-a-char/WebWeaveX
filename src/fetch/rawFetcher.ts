/**
 * Converted from Python: core/fetch/raw_fetcher.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { FetchResponse } from "./base.js";

export function fetchRaw(text: any, source_url: any = ""): any {
  return new FetchResponse("raw", py.or2(source_url, () => ("")), 200, "text/plain", py.or2(text, () => ("")), true, "", {"length": py.toStr(py.len(py.or2(text, () => (""))))}).to_dict();
}
export { FetchResponse };
