import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { join } from "node:path";

describe("protected smoke: src/memory/memoryQuery.ts", () => {
  it("module file exists", () => {
    expect(existsSync(join(process.cwd(), "src/memory/memoryQuery.ts"))).toBe(true);
  });
});
