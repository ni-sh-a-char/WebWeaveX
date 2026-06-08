import { runRuntimeCognitionTick } from "../cognition/runtimeCognitionEngine.js";

export function executeCognitionVm(
  session: Record<string, unknown>,
  program: Array<Record<string, unknown>>,
): Record<string, unknown> {
  const results = program.map((step, i) =>
    runRuntimeCognitionTick(session, [step], [{ id: String(i), type: "cognition" }]),
  );
  return { results, bounded: true, steps: program.length };
}
