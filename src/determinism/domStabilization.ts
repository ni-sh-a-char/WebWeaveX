import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

const UUID_RE =
  /[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}/gi;
const TIMESTAMP_RE =
  /\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b/g;
const REACT_RE = /data-react[a-z0-9-]*="[^"]*"/gi;
const VUE_RE = /data-v-[a-z0-9]+="[^"]*"/gi;
const ANGULAR_RE = /\s(?:ng-version|_ngcontent[a-z0-9-]*|_nghost[a-z0-9-]*)="[^"]*"/gi;
const NONCE_RE = /\snonce="[^"]*"/gi;
const SCRIPT_BODY_RE = /<script\b[^>]*>[\s\S]*?<\/script>/gi;

/** Production DOM stabilization for deterministic replay fingerprints. */
export function stabilizeDomHtml(html: string): string {
  let s = html;
  s = s.replace(UUID_RE, "uuid-stabilized");
  s = s.replace(TIMESTAMP_RE, "timestamp-stabilized");
  s = s.replace(REACT_RE, "");
  s = s.replace(VUE_RE, "");
  s = s.replace(ANGULAR_RE, "");
  s = s.replace(NONCE_RE, "");
  s = s.replace(SCRIPT_BODY_RE, "<script>stabilized</script>");
  s = s.replace(/<!--[\s\S]*?-->/g, "");
  s = s.replace(/\s+/g, " ").trim();
  return s;
}

export function normalizeDom(html: string): string {
  return stabilizeDomHtml(html);
}

export function computeStableDomHash(html: string): string {
  return computeDeterministicHash(stabilizeDomHtml(html));
}

/** SPA fingerprint: hash of stabilized DOM (not raw HTML). */
export function computeSpaFingerprint(html: string): string {
  return computeStableDomHash(html);
}
