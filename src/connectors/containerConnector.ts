import { extractDockerRuntime } from "./dockerConnector.js";

export function extractContainerRuntime(
  runtime = "docker",
  snapshot: Record<string, unknown> = {},
): Record<string, unknown> {
  const n = runtime.toLowerCase();
  try {
    if (["docker", "podman", "oci"].includes(n)) {
      return { ...extractDockerRuntime(snapshot), runtime: n };
    }
  } catch {
    /* bounded degrade */
  }
  return { runtime: n, containers: [], degraded: true, bounded: true };
}
