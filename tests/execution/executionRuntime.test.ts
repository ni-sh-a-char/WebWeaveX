import { describe, expect, it } from "vitest";
import { runExecutionRuntime } from "../../src/execution/executionRuntime.js";

describe("runExecutionRuntime", () => {
  it("allowlists actions", () => {
    const out = runExecutionRuntime([
      { action: "simulate" },
      { action: "eval" },
    ]);
    expect(out.denied).toContain("eval");
    expect(out.results).toHaveLength(1);
  });
});
