export function recoverParserState(
  failedParser: string,
  checkpoint: Record<string, unknown>,
): Record<string, unknown> {
  return {
    recovered_parser: failedParser,
    checkpoint,
    recovered: true,
    bounded: true,
  };
}
