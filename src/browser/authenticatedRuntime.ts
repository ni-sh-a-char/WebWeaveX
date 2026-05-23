import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { encryptValue, decryptValue } from "../crypto/kaalka.js";
import stringify from "fast-json-stable-stringify";

export type SessionState = {
  cookies?: unknown[];
  headers?: Record<string, string>;
  auth_tokens?: unknown[];
  localStorage?: Record<string, string>;
  sessionStorage?: Record<string, string>;
};

export function saveAuthenticatedRuntime(
  path: string,
  state: SessionState,
  encryptionKey: string,
): { path: string; algorithm: string; bounded: boolean } {
  const payload = encryptValue(stringify(state), encryptionKey);
  const envelope = stringify({
    algorithm: "kaalka",
    encrypted: payload.encrypted,
    version: "2.0.0",
  });
  writeFileSync(path, envelope, "utf-8");
  return { path, algorithm: "kaalka", bounded: true };
}

export function loadAuthenticatedRuntime(
  path: string,
  encryptionKey: string,
): SessionState {
  if (!existsSync(path)) {
    return { cookies: [], headers: {}, auth_tokens: [] };
  }
  const raw = JSON.parse(readFileSync(path, "utf-8")) as { encrypted: string };
  const dec = decryptValue(raw.encrypted, encryptionKey);
  return JSON.parse(dec.decrypted) as SessionState;
}

export function rotateAuthenticatedSession(
  session: SessionState,
): SessionState {
  return {
    ...session,
    headers: { ...(session.headers ?? {}), "x-kaalka-rotated": "1" },
  };
}
