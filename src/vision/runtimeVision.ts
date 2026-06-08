export function extractVisionMetadata(input: Record<string, unknown>): Record<string, unknown> {
  const frames = (input.frames as unknown[]) ?? [];
  return {
    frame_count: frames.length,
    vision_id: input.id ?? "vision",
    available: frames.length > 0 || input.width != null,
    bounded: true,
  };
}
