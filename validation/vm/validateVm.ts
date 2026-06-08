import { runSemanticVm } from "../../src/vm/semanticVmEngine.js";
import { executeCognitionVm } from "../../src/vm/cognitionExecutionVm.js";
import { executeReplayVm } from "../../src/vm/replayExecutionVm.js";
import { executeDistributedVm } from "../../src/vm/distributedExecutionVm.js";
import { executeContinuationVm } from "../../src/vm/runtimeContinuationVm.js";
import { executeOrchestrationVm } from "../../src/vm/semanticOrchestrationVm.js";

const semantic = runSemanticVm([
  { opcode: "LINK", operand: { from: "a", to: "b" } },
]);

const results = {
  semantic_vm: semantic.bounded === true,
  cognition_vm: executeCognitionVm({}, [{ s: 1 }]).bounded === true,
  replay_vm: executeReplayVm([{ id: "1", type: "t" }]).bounded === true,
  distributed_vm: executeDistributedVm([], []).synchronized === true,
  continuation_vm: executeContinuationVm({ x: 1 }, { y: 2 }).continued === true,
  orchestration_vm: executeOrchestrationVm([{ a: 1 }]).bounded === true,
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
