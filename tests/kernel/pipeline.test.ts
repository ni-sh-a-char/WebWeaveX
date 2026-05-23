import { describe, expect, it } from "vitest";
import { runCanonicalPipeline } from "../../src/kernel/runtimePipeline.js";

describe("runCanonicalPipeline", () => {
  it("text kind", async () => {
    const out = await runCanonicalPipeline({ source: "hello", sourceType: "text" });
    expect(out.bounded).toBe(true);
    expect(out.ingestion.type).toBe("text");
  });
});
