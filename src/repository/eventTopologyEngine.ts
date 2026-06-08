/**
 * Converted from Python: core/repository/event_topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { parseSource } from "../parsers/index.js";
import { buildTopologyCognition } from "./topologyCognitionEngine.js";

let _EVENT_KEYS: any = ["kafka", "rabbitmq", "sns", "sqs", "nats", "celery", "rq", "bullmq"];
export function inferEventTopology(text: any, path: any = ""): any {
  var parsed: any = parseSource(py.or2(text, () => ("")), path);
  var imports: any = py.iter(py.get(py.get(parsed, "symbols", {}), "imports", [])).map((i: any) => String(py.toStr(i)).toLowerCase());
  var deps: any = py.iter(py.get(py.get(parsed, "dependencies", {}), "dependencies", [])).map((d: any) => String(py.toStr(d)).toLowerCase());
  var frameworks: any = py.iter(py.get(py.get(parsed, "frameworks", {}), "frameworks", [])).map((f: any) => String(py.toStr(f)).toLowerCase());
  var evidence: any = py.add(py.add(imports, deps), frameworks);
  var buses: any = py.sorted(py.toSet(py.iter(["kafka", "rabbitmq", "sns", "sqs", "nats"]).filter((k: any) => py.any(py.iter(evidence).map((e: any) => py.contains(e, k)))).map((k: any) => k)));
  var queues: any = py.sorted(py.toSet(py.iter(["celery", "rq", "bullmq"]).filter((k: any) => py.any(py.iter(evidence).map((e: any) => py.contains(e, k)))).map((k: any) => k)));
  if ((!py.truthy(buses) && !py.truthy(queues))) {
    var src: any = String(py.or2(text, () => (""))).toLowerCase();
    buses = py.iter(["kafka", "rabbitmq", "sns", "sqs", "nats"]).filter((k: any) => py.contains(src, k)).map((k: any) => k);
    queues = py.iter(["celery", "rq", "bullmq"]).filter((k: any) => py.contains(src, k)).map((k: any) => k);
  }
  var nodes: any = py.sorted(py.toSet(py.add(buses, queues)));
  var parser_backed: any = py.truthy(py.or2(imports, () => (py.or2(deps, () => (frameworks)))));
  var evidence_kind: any = (py.truthy(parser_backed) ? "parser_imports" : "text_fallback");
  var cognition: any = buildTopologyCognition(text, path, nodes, nodes);
  py.setItem(cognition, "evidence_trace", py.get(cognition, "evidence", []));
  py.setItem(cognition, "evidence", evidence_kind);
  py.setItem(cognition, "event_buses", buses);
  py.setItem(cognition, "queue_systems", queues);
  return cognition;
}
export { buildTopologyCognition, parseSource };
