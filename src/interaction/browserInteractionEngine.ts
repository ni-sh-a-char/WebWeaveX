/**
 * Converted from Python: core/interaction/browser_interaction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let DEFAULT_TIMEOUT_MS: any = 30000;
export let MAX_ACTIONS: any = 1000;
export function recordInteraction(action: any, selector: any, metadata: any = null, step: any = 0): any {
  return {"id": `interaction_${py.toStr(step)}`, "timestamp": step, "action": py.strip(py.toStr(action)), "selector": py.strip(py.toStr(selector)), "metadata": py.pyDict(py.or2(metadata, () => ({}))), "bounded": true};
}
export function buildInteractionPlan(actions: any): any {
  var normalized: any[] = [];
  var index: any;
  var action: any;
  for ([index, action] of py.enumerate(py.slice(actions, null, MAX_ACTIONS))) {
    py.listAppend(normalized, recordInteraction(py.toStr(py.get(action, "type", py.get(action, "action", ""))), py.toStr(py.get(action, "selector", "")), {"value": py.get(action, "value")}, index));
  }
  return {"interaction_plan": normalized, "bounded": true};
}
export function _boundedTimeout(timeout_ms: any): any {
  var timeout: any = py.toInt(py.or2(timeout_ms, () => (DEFAULT_TIMEOUT_MS)));
  return py.min([py.max([timeout, 1]), DEFAULT_TIMEOUT_MS]);
}
export function clickElement(page: any, selector: any, timeout_ms: any = null): any {
  var timeout: any = _boundedTimeout(timeout_ms);
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("click") in (page as object) || typeof (page as Record<string, unknown>)[String("click")] === "function")))) {
    page.click(selector, timeout);
  }
  return {"action": "click", "selector": selector, "timeout_ms": timeout, "bounded": true};
}
export function fillInput(page: any, selector: any, value: any, timeout_ms: any = null): any {
  var timeout: any = _boundedTimeout(timeout_ms);
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("fill") in (page as object) || typeof (page as Record<string, unknown>)[String("fill")] === "function")))) {
    page.fill(selector, py.slice(py.toStr(value), null, 5000), timeout);
  }
  return {"action": "fill", "selector": selector, "value": py.slice(py.toStr(value), null, 5000), "timeout_ms": timeout, "bounded": true};
}
export function selectOption(page: any, selector: any, value: any, timeout_ms: any = null): any {
  var timeout: any = _boundedTimeout(timeout_ms);
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("select_option") in (page as object) || typeof (page as Record<string, unknown>)[String("select_option")] === "function")))) {
    page.select_option(selector, py.slice(py.toStr(value), null, 5000), timeout);
  }
  return {"action": "select", "selector": selector, "value": py.slice(py.toStr(value), null, 5000), "timeout_ms": timeout, "bounded": true};
}
export function hoverElement(page: any, selector: any, timeout_ms: any = null): any {
  var timeout: any = _boundedTimeout(timeout_ms);
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("hover") in (page as object) || typeof (page as Record<string, unknown>)[String("hover")] === "function")))) {
    page.hover(selector, timeout);
  }
  return {"action": "hover", "selector": selector, "timeout_ms": timeout, "bounded": true};
}
export function waitForSelector(page: any, selector: any, timeout_ms: any = null): any {
  var timeout: any = _boundedTimeout(timeout_ms);
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("wait_for_selector") in (page as object) || typeof (page as Record<string, unknown>)[String("wait_for_selector")] === "function")))) {
    page.wait_for_selector(selector, timeout);
  }
  return {"action": "wait", "selector": selector, "timeout_ms": timeout, "bounded": true};
}
