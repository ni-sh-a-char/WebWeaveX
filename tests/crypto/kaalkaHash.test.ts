import { describe, expect, it } from "vitest";
import { computeKaalkaHash, computeKaalkaHashPayload } from "../../src/crypto/kaalkaHash.js";

describe("kaalka hash", () => {
  it("stable hash", () => {
    expect(computeKaalkaHash("x")).toBe(computeKaalkaHash("x"));
    expect(computeKaalkaHashPayload({ a: 1 })).toHaveLength(64);
  });
});
