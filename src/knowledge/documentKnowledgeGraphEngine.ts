/**
 * Converted from Python: core/knowledge/document_knowledge_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_NODES: any = 10000;
export function buildDocumentKnowledgeGraph(structure: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var sections: any = py.get(structure, "sections", []);
  var idx: any;
  var section: any;
  for ([idx, section] of py.enumerate(sections)) {
    var node_id: any = `section_${py.toStr(idx)}`;
    py.listAppend(nodes, {"id": node_id, "title": py.get(section, "title")});
    if ((idx > 0)) {
      py.listAppend(edges, {"from": `section_${py.toStr(py.sub(idx, 1))}`, "to": node_id, "relation": "next_section"});
    }
  }
  return {"nodes": py.slice(nodes, null, MAX_NODES), "edges": py.slice(edges, null, MAX_NODES), "bounded": true};
}
