import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { join } from "node:path";

describe("protected smoke: src/browser/extractWeb.ts", () => {
  it("module file exists", () => {
    expect(existsSync(join(process.cwd(), "src/browser/extractWeb.ts"))).toBe(true);
  });
});
