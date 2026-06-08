/**
 * Converted from Python: core/repository/runtime_semantic_ir_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { inferRuntimeEvents } from "./runtimeEventEngine.js";
import { inferInfraExecution } from "./infraExecutionEngine.js";

export function compileRuntimeSemanticIr(dependencies: any, parser_evidence: any): any {
  var events: any = inferRuntimeEvents(dependencies, parser_evidence);
  var infra: any = inferInfraExecution(dependencies, parser_evidence);
  return {"events": events, "infra": infra, "dependencies": py.sorted(dependencies), "deterministic": true};
}
export { inferInfraExecution, inferRuntimeEvents };
