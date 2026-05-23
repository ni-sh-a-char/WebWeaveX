import { describe, expect, it } from "vitest";
import { runCanonicalPipeline } from "../../src/kernel/runtimePipeline.js";

describe("pipeline kinds", () => {
  it("document and auto-detect http", async () => {
    const doc = await runCanonicalPipeline({
      source: "readme.md",
      sourceType: "document",
    });
    expect(doc.ingestion.type).toBe("document");

    const auto = await runCanonicalPipeline({ source: "https://example.org", sourceType: "auto" });
    expect(auto.ingestion.type).toBe("web");
  });
});
