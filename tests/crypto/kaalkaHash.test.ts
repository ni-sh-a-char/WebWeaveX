import { describe, expect, it } from "vitest";
import {
  computeDeterministicHash,
  computeDeterministicHashPayload,
} from "../../src/crypto/kaalkaRuntime.js";

describe("kaalka hash", () => {
  it("stable hash", () => {
    expect(computeDeterministicHash("x")).toBe(computeDeterministicHash("x"));
    expect(computeDeterministicHashPayload({ a: 1 })).toHaveLength(64);
  });
});
