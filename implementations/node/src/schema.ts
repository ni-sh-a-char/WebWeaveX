export interface Entity {
  type: string;
  value: string;
}

export interface Chunk {
  text: string;
  index: number;
  start: number;
  end: number;
}

export interface GraphEdge {
  source: string;
  target: string;
  weight: number;
  directed?: boolean;
}

export interface GraphResult {
  nodes: Entity[];
  edges: GraphEdge[];
}

export interface Metadata {
  url: string;
  version: string;
}

export interface CrawlResult {
  url: string;
  text: string;
  chunks?: Chunk[];
  entities?: Entity[];
  graph?: GraphResult;
  metadata?: Metadata;
}

export interface CompareResult {
  urls: string[];
  common_entities: Entity[];
  unique_entities: Record<string, Entity[]>;
}

export interface DiffResult {
  url1: string;
  url2: string;
  common_entities: Entity[];
  unique_to_url1: Entity[];
  unique_to_url2: Entity[];
}

export interface WeaveResult {
  urls: string[];
  text: string;
  chunks: Chunk[];
  entities: Entity[];
  graph: GraphResult;
}

export interface ToolResult {
  tool: string;
  success: boolean;
  result: any;
  error?: string;
}
