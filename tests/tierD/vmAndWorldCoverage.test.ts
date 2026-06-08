import { describe, expect, it } from "vitest";
import { executeDistributedVm } from "../../src/vm/distributedExecutionVm.js";
import { executeReplayVm } from "../../src/vm/replayExecutionVm.js";
import { executeContinuationVm } from "../../src/vm/runtimeContinuationVm.js";
import { executeOrchestrationVm } from "../../src/vm/semanticOrchestrationVm.js";
import { cognizeRuntimeEnvironment } from "../../src/worldModel/runtimeEnvironmentCognition.js";
import { loadStreamRuntime, saveStreamRuntime } from "../../src/streaming/streamPersistence.js";
import { mkdtempSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { makeStreamEvent } from "../../src/streaming/streamCapture.js";

describe("vm fleet and world cognition coverage", () => {
  it("executes all VM adapters", () => {
    expect(executeDistributedVm([{ id: "n" }], [{ id: "e" }]).synchronized).toBe(true);
    expect(executeReplayVm([{ id: "1", type: "t" }]).bounded).toBe(true);
    expect(executeContinuationVm({ a: 1 }, { b: 2 }).continued).toBe(true);
    expect(executeOrchestrationVm([{ x: 1 }, { y: 2 }]).depth).toBe(2);
    expect(cognizeRuntimeEnvironment({ id: "env", region: "us" }).bounded).toBe(true);
  });

  it("stream persistence error branch", () => {
    const dir = mkdtempSync(join(tmpdir(), "wwx-cov-"));
    const path = join(dir, "bad.json");
    saveStreamRuntime(path, { events: [makeStreamEvent(0, "s", "in", "{}", "c")] }, "key");
    const loaded = loadStreamRuntime(join(dir, "missing.json"), "key");
    expect(loaded.events).toHaveLength(0);
    rmSync(dir, { recursive: true, force: true });
  });
});
