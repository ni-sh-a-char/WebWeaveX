import { describe, expect, it } from "vitest";
import { normalizeNetwork } from "../../src/determinism/normalization.js";

describe("normalizeNetwork", () => {
  it("sorts by method and url", () => {
    const out = normalizeNetwork([
      { url: "/b", method: "GET" },
      { url: "/a", method: "POST" },
      { url: "/a", method: "GET" },
    ]);
    expect(out[0]?.url).toBe("/a");
    expect(out[0]?.method).toBe("GET");
  });
});
