import { describe, expect, it } from "vitest";
import { stableSerialize } from "../../src/determinism/normalization.js";
import { computeDeterministicHash } from "../../src/crypto/kaalkaRuntime.js";

describe("volatile key stripping", () => {
  it("drops volatile keys for stable hash", () => {
    const a = { ok: 1, timestamp: 1, uuid: "x", nested: { runtime_id: "r" } };
    const b = { ok: 1, nested: {} };
    expect(computeDeterministicHash(a)).toBe(computeDeterministicHash(b));
    expect(stableSerialize(a)).toBe(stableSerialize(b));
  });
});
