import { describe, expect, it, vi } from "vitest";

vi.mock("../../src/browser/extractWeb.js", () => ({
  extractWeb: vi.fn(async () => ({
    bounded: true,
    unified_runtime_graph: { nodes: [{ id: "n" }], edges: [] },
    runtime: { available: true },
    pipeline_hash: "h",
    global_runtime_fingerprint: "fp",
  })),
}));

import { runCanonicalPipeline } from "../../src/kernel/runtimePipeline.js";

describe("pipeline detectKind branches", () => {
  it("text and document extensions", async () => {
    const text = await runCanonicalPipeline({ source: "notes.txt" });
    expect(text.ingestion.type).toBe("document");
    expect((text.runtime as Record<string, unknown>).available).toBe(false);

    const pdf = await runCanonicalPipeline({ source: "/data/report.pdf" });
    expect(pdf.ingestion.type).toBe("document");

    const plain = await runCanonicalPipeline({ source: "raw-input", sourceType: "text" });
    expect(plain.ingestion.type).toBe("text");
  });

  it("web via path url", async () => {
    const web = await runCanonicalPipeline({ source: "https://example.com/page" });
    expect(web.ingestion.type).toBe("web");
  });
});
