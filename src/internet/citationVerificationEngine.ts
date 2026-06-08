/**
 * Converted from Python: core/internet/citation_verification_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function verifyCitations(text: any): any {
  var urls: any = py.sorted(py.toSet(py.reFindall("https?://[^\\s\\)\\]\\\"']+", py.or2(text, () => ("")), "")));
  var dois: any = py.sorted(py.toSet(py.reFindall("10\\.\\d{4,9}/[-._;()/:A-Z0-9]+", py.or2(text, () => ("")), "i")));
  return {"url_count": py.len(urls), "doi_count": py.len(dois), "verified": py.truthy(py.or2(urls, () => (dois))), "deterministic_inputs": [`urls=${py.toStr(py.len(urls))}`, `dois=${py.toStr(py.len(dois))}`]};
}
