import { computeKaalkaHash } from "../crypto/kaalkaHash.js";

const UUID_RE =
  /[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}/gi;
const TIMESTAMP_RE =
  /\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b/g;
const REACT_RE = /data-react[a-z]*="[^"]*"/gi;
const VUE_RE = /data-v-[a-z0-9]+="[^"]*"/gi;

export function stabilizeDomHtml(html: string): string {
  let s = html;
  s = s.replace(UUID_RE, "uuid-stabilized");
  s = s.replace(TIMESTAMP_RE, "timestamp-stabilized");
  s = s.replace(REACT_RE, "");
  s = s.replace(VUE_RE, "");
  s = s.replace(/<!--[\s\S]*?-->/g, "");
  s = s.replace(/\s+/g, " ").trim();
  return s;
}

export function computeStableDomHash(html: string): string {
  return computeKaalkaHash(stabilizeDomHtml(html));
}
