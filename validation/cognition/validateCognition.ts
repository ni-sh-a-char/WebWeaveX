import { runRuntimeCognitionTick } from "../../src/cognition/runtimeCognitionEngine.js";
import { recoverRuntime } from "../../src/runtime/runtimeRecoveryEngine.js";
import { replaySemanticEvents } from "../../src/runtime/semanticReplayVm.js";

const tick = runRuntimeCognitionTick({ session: { ok: true } }, [{ a: 1 }], [
  { id: "e1", type: "tick" },
]);
const recovery = recoverRuntime("failed", ["e"]);
const replay = replaySemanticEvents([{ id: "e1", type: "tick" }]);

const results = {
  cognition: tick.bounded === true,
  // authority (core/runtime/runtime_recovery_engine.py): recovery reports the
  // recovered state with deterministic transition accounting
  recovery: recovery.recovered_state === "failed" && recovery.transitions === 3 && recovery.deterministic === true,
  replay: (replay.event_count as number) === 1,
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
