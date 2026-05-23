import { describe, expect, it, vi } from "vitest";
import { runCanonicalPipeline } from "../../src/kernel/runtimePipeline.js";

vi.mock("../../src/browser/extractWeb.js", () => ({
  extractWeb: vi.fn(async () => ({
    bounded: true,
    unified_runtime_graph: { nodes: [{ id: "n1" }], edges: [] },
    pipeline_hash: "ph",
    global_runtime_fingerprint: "fp",
  })),
}));

describe("pipeline web", () => {
  it("web path", async () => {
    const out = await runCanonicalPipeline({
      source: "https://example.com",
      sourceType: "web",
    });
    expect(out.ingestion.type).toBe("web");
    expect(out.bounded).toBe(true);
  });
});
