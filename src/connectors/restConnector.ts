export async function extractRestRuntime(
  url: string,
): Promise<{ available: boolean; url: string; bounded: boolean }> {
  try {
    const res = await fetch(url, { method: "GET" });
    return { available: res.ok, url, bounded: true };
  } catch {
    return { available: false, url, bounded: true };
  }
}
