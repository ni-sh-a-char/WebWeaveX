import { readFileSync, writeFileSync, existsSync } from "node:fs";
import stringify from "fast-json-stable-stringify";
import { encryptValue, decryptValue } from "../crypto/kaalkaRuntime.js";

export function saveRuntimeMemory(
  path: string,
  memory: Record<string, unknown>,
  encryptionKey: string,
): { path: string; bounded: boolean } {
  const payload = encryptValue(memory, encryptionKey);
  writeFileSync(
    path,
    stringify({ algorithm: "kaalka", encrypted: payload.encrypted, version: "2.0.0" }),
    "utf-8",
  );
  return { path, bounded: true };
}

export function loadRuntimeMemory(path: string, encryptionKey: string): Record<string, unknown> {
  if (!existsSync(path)) {
    return { memory: { runtime_history: [] }, stable_hash: "", bounded: true };
  }
  const raw = JSON.parse(readFileSync(path, "utf-8")) as { encrypted: string };
  const dec = decryptValue(raw.encrypted, encryptionKey);
  return JSON.parse(dec.decrypted) as Record<string, unknown>;
}
