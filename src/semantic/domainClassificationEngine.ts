/**
 * Converted from Python: core/semantic/domain_classification_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

var DOMAIN_RULES: any = [["saas", py.regex("\\b(saas|subscription|tenant|workspace)\\b", "i")], ["finance", py.regex("\\b(invoice|ledger|payment|billing|revenue)\\b", "i")], ["analytics", py.regex("\\b(analytics|dashboard|kpi|metrics|report)\\b", "i")], ["infrastructure", py.regex("\\b(kubernetes|terraform|infra|cluster|deploy)\\b", "i")], ["devops", py.regex("\\b(ci/cd|pipeline|build|release|deploy)\\b", "i")], ["crm", py.regex("\\b(crm|customer|lead|opportunity|contact)\\b", "i")], ["ecommerce", py.regex("\\b(cart|checkout|product|order|sku)\\b", "i")], ["support", py.regex("\\b(ticket|support|helpdesk|incident)\\b", "i")], ["security", py.regex("\\b(security|auth|oauth|permission|role)\\b", "i")], ["developer_tooling", py.regex("\\b(ide|repository|api|sdk|debug)\\b", "i")]];
export function classifySemanticDomain(text: any = "", signals: any = null): any {
  signals = py.or2(signals, () => ([]));
  var combined: any = `${py.toStr(text)} ${py.toStr(py.join(" ", signals))}`;
  var scores: Record<string, any> = {};
  var domain: any;
  var pattern: any;
  for ([domain, pattern] of py.iter(DOMAIN_RULES)) {
    var matches: any = py.len(pattern.findall(combined));
    if (py.truthy(matches)) {
      py.setItem(scores, domain, matches);
    }
  }
  if (!py.truthy(scores)) {
    var primary: any = "saas";
  } else {
    primary = py.at(py.at(py.sorted(py.items(scores), {key: ((item: any) => [(-py.at(item, 1)), py.at(item, 0)]) as (item: any) => any}), 0), 0);
  }
  return {"domain": primary, "scores": scores, "signals": signals, "bounded": true};
}
