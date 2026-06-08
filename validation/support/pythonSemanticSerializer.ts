import { createHash } from "node:crypto";

/** Compact JSON matching Python json.dumps(..., sort_keys=True, separators=(",", ":")). */
export function pythonCompactSerialize(value: unknown): string {
  if (value === null || value === undefined) return "null";
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "number") return Number.isFinite(value) ? String(value) : "null";
  if (typeof value === "string") return JSON.stringify(value);
  if (Array.isArray(value)) {
    return `[${value.map((v) => pythonCompactSerialize(v)).join(",")}]`;
  }
  if (typeof value === "object") {
    const obj = value as Record<string, unknown>;
    const keys = Object.keys(obj).sort();
    return `{${keys.map((k) => `${JSON.stringify(k)}:${pythonCompactSerialize(obj[k])}`).join(",")}}`;
  }
  return JSON.stringify(String(value));
}

/** Python json.dumps(..., sort_keys=True) default separators (", ", ": "). */
export function pythonStyleSerialize(value: unknown): string {
  if (value === null || value === undefined) return "null";
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "number") return Number.isFinite(value) ? String(value) : "null";
  if (typeof value === "string") return JSON.stringify(value);
  if (Array.isArray(value)) {
    return `[${value.map((v) => pythonStyleSerialize(v)).join(", ")}]`;
  }
  if (typeof value === "object") {
    const obj = value as Record<string, unknown>;
    const keys = Object.keys(obj).sort();
    return `{${keys.map((k) => `${JSON.stringify(k)}: ${pythonStyleSerialize(obj[k])}`).join(", ")}}`;
  }
  return JSON.stringify(String(value));
}

export function pythonSha256Hex(data: string, truncate = 0): string {
  const hex = createHash("sha256").update(data, "utf8").digest("hex");
  return truncate > 0 ? hex.slice(0, truncate) : hex;
}

/** Kaalka hash when Python passes a pre-serialized JSON string to compute_kaalka_hash. */
export function pythonKaalkaHashFromJsonString(jsonBody: string): string {
  return pythonSha256Hex(jsonBody);
}
