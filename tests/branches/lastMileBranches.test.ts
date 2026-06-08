import { describe, expect, it } from "vitest";
import { RuntimeGraphContract } from "../../src/contracts/graphContracts.js";
import { dequeueExtraction } from "../../src/distributed/extractionQueueEngine.js";
import { restoreSemanticSnapshot } from "../../src/semantic/semanticSnapshot.js";
import { detectRepositoryLanguages } from "../../src/repository/repositoryLanguageDetection.js";
import { buildStreamTimeline } from "../../src/streaming/streamReplay.js";
import { recoverRuntime } from "../../src/runtime/runtimeRecoveryEngine.js";

describe("last mile branches", () => {
  it("graph contract sort permutations", () => {
    const g = RuntimeGraphContract.normalize({
      nodes: [{ id: "b" }, { id: "a", type: "t", name: "n" }],
      edges: [{ target: "b", source: "a", type: "x" }],
    });
    expect(g.nodes[0]!.id).toBe("a");
  });

  it("queue dequeue empty", () => {
    expect(dequeueExtraction([]).task).toBeNull();
  });

  it("misc branch helpers", () => {
    expect(restoreSemanticSnapshot({ state: { a: 1 } }).a).toBe(1);
    expect(detectRepositoryLanguages([]).primary).toBe("");
    expect(buildStreamTimeline([]).count).toBe(0);
    expect(recoverRuntime("initialized").recovered_state).toBe("initialized");
    expect(recoverRuntime("initialized").transitions).toBe(2);
  });
});
