/**
 * Converted from Python: core/adaptive/modal_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_RETRIES: any = 5;
let _MODAL_CLOSE_SELECTORS: any = ["#cookie-accept", "[aria-label='Close']", "button.accept", ".modal-close"];
export function recoverModalRuntime(page: any, html: any = ""): any {
  var recovered: any[] = [];
  var retries: any = 0;
  var modals: any[] = [];
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_modals") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_modals")] === "function")))) {
    modals = [...py.iter(page._test_modals)];
  }
  var selector: any;
  for (selector of py.iter(_MODAL_CLOSE_SELECTORS)) {
    if (py.ge(retries, MAX_RETRIES)) {
      break;
    }
    if ((py.truthy(_selectorInHtml(selector, html)) || py.truthy(modals))) {
      if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("click") in (page as object) || typeof (page as Record<string, unknown>)[String("click")] === "function")))) {
        try {
          page.click(selector);
        } catch (_e: any) {
        }
      }
      if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_modals") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_modals")] === "function"))) {
        page._test_modals = [];
      }
      py.listAppend(recovered, {"selector": selector, "recovered": true});
      retries = py.add(retries, 1);
      break;
    }
  }
  return {"recovered": recovered, "retries": retries, "bounded": true};
}
export function _selectorInHtml(selector: any, html: any): any {
  var token: any = py.at(py.split(py.at(py.split(py.strip(selector, "#.[]"), "'"), 0), "\""), 0);
  return py.contains(String(html).toLowerCase(), String(token).toLowerCase());
}
