export function cognizeRuntimeEnvironment(env: Record<string, unknown>): Record<string, unknown> {
  return {
    environment_id: env.id ?? "default",
    signals: Object.keys(env).sort(),
    bounded: true,
  };
}
