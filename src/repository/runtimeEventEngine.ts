/**
 * Converted from Python: core/repository/runtime_event_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let EVENT_KEYWORDS: any = py.toSet(new Set(["kafka", "rabbitmq", "sns", "sqs", "nats", "celery", "rq"]));
export function inferRuntimeEvents(dependencies: any, parser_evidence: any): any {
  var observed: any = py.sorted(py.iter(dependencies).filter((dep: any) => py.contains(EVENT_KEYWORDS, String(dep).toLowerCase())).map((dep: any) => dep));
  return {"events": observed, "evidence": py.sorted(py.toSet(parser_evidence)), "grounded": py.truthy(parser_evidence), "deterministic": true};
}
