export function detectBuildSystems(files: Array<{ path: string }>): Record<string, unknown> {
  const systems = new Set<string>();
  for (const f of files) {
    const name = f.path.split(/[/\\]/).pop() ?? "";
    if (name === "package.json") systems.add("npm");
    if (name === "pyproject.toml" || name === "setup.py") systems.add("python");
    if (name === "Cargo.toml") systems.add("cargo");
    if (name === "go.mod") systems.add("go");
  }
  return { build_systems: [...systems].sort(), bounded: true };
}
