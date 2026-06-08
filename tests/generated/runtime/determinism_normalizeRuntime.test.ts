import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { join } from "node:path";

describe("protected smoke: src/determinism/normalizeRuntime.ts", () => {
  it("module file exists", () => {
    expect(existsSync(join(process.cwd(), "src/determinism/normalizeRuntime.ts"))).toBe(true);
  });
});
