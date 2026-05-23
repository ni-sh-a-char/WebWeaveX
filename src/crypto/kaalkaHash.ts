import { createHash } from "node:crypto";
import stringify from "fast-json-stable-stringify";
import { normalizeRuntimeValue } from "./kaalka.js";

const MAX_HASH_INPUT_BYTES = 10_000_000;

export function computeKaalkaHash(value: string): string {
  const normalized = normalizeRuntimeValue(value);
  const buf = Buffer.from(normalized, "utf-8").subarray(0, MAX_HASH_INPUT_BYTES);
  return createHash("sha256").update(buf).digest("hex");
}

export function computeKaalkaHashPayload(payload: unknown): string {
  return computeKaalkaHash(stringify(payload));
}
