/**
 * Converted from Python: core/interaction/modal_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_MODALS: any = 100;
let _MODAL_RE: any = py.regex("(cookie|modal|dialog|overlay|auth)", "i");
export function detectModals(page: any): any {
  var modals: any[] = [];
  var html: any = "";
  if ((page !== null && page !== undefined)) {
    if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_modals") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_modals")] === "function"))) {
      modals = py.slice([...py.iter(page._test_modals)], null, MAX_MODALS);
      return {"modals": modals, "bounded": true};
    }
    if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_html") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_html")] === "function"))) {
      html = py.toStr(page._test_html);
    }
  }
  var match: any;
  for (match of py.iter(py.slice(_MODAL_RE.findall(html), null, MAX_MODALS))) {
    py.listAppend(modals, {"type": String(match).toLowerCase(), "selector": `[data-${py.toStr(String(match).toLowerCase())}]`});
  }
  return {"modals": modals, "bounded": true};
}
export function closeModal(page: any, selector: any): any {
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("click") in (page as object) || typeof (page as Record<string, unknown>)[String("click")] === "function")) && py.truthy(selector))) {
    try {
      page.click(selector);
    } catch (_e: any) {
    }
  }
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_modals") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_modals")] === "function")))) {
    page._test_modals = [];
  }
  return {"closed": true, "selector": selector, "bounded": true};
}
