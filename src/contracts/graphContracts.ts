export type RuntimeNode = Record<string, unknown> & { id?: string; type?: string; name?: string };
export type RuntimeEdge = Record<string, unknown> & {
  source?: string;
  from?: string;
  target?: string;
  to?: string;
  type?: string;
};

export type RuntimeGraph = {
  nodes: RuntimeNode[];
  edges: RuntimeEdge[];
  bounded?: boolean;
};

export const RuntimeGraphContract = {
  normalize(graph: RuntimeGraph): RuntimeGraph {
    const nodes = [...(graph.nodes ?? [])].sort((a, b) => {
      const ka = `${a.id ?? ""}|${a.type ?? ""}|${a.name ?? ""}`;
      const kb = `${b.id ?? ""}|${b.type ?? ""}|${b.name ?? ""}`;
      return ka.localeCompare(kb);
    });
    const edges = [...(graph.edges ?? [])].sort((a, b) => {
      const ka = `${a.source ?? a.from ?? ""}|${a.target ?? a.to ?? ""}|${a.type ?? ""}`;
      const kb = `${b.source ?? b.from ?? ""}|${b.target ?? b.to ?? ""}|${b.type ?? ""}`;
      return ka.localeCompare(kb);
    });
    return { nodes, edges, bounded: true };
  },
};
