import {
  loadAuthenticatedRuntime,
  rotateAuthenticatedSession,
  saveAuthenticatedRuntime,
  type SessionState,
} from "./authenticatedRuntime.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaRuntime.js";

export type RuntimeSessionEnvelope = SessionState & {
  session_id: string;
  bounded: boolean;
};

export function createRuntimeSession(state: SessionState = {}): RuntimeSessionEnvelope {
  const normalized: SessionState = {
    cookies: state.cookies ?? [],
    headers: state.headers ?? {},
    auth_tokens: state.auth_tokens ?? [],
    localStorage: state.localStorage ?? {},
    sessionStorage: state.sessionStorage ?? {},
  };
  return {
    ...normalized,
    session_id: computeKaalkaHashPayload(normalized),
    bounded: true,
  };
}

export function persistRuntimeSession(
  path: string,
  session: RuntimeSessionEnvelope,
  encryptionKey: string,
): { path: string; session_id: string; bounded: boolean } {
  const result = saveAuthenticatedRuntime(path, session, encryptionKey);
  return { path: result.path, session_id: session.session_id, bounded: true };
}

export function restoreRuntimeSession(
  path: string,
  encryptionKey: string,
): RuntimeSessionEnvelope {
  const loaded = loadAuthenticatedRuntime(path, encryptionKey);
  return createRuntimeSession(loaded);
}

export function rotateRuntimeSession(session: RuntimeSessionEnvelope): RuntimeSessionEnvelope {
  return createRuntimeSession(rotateAuthenticatedSession(session));
}
