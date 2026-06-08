/**
 * Converted from Python: core/repository/architecture_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructRepository } from "./repositoryReconstructionEngine.js";

export function reasonArchitecture(text: any, source_url: any = ""): any {
  var repo: any = reconstructRepository(text, source_url);
  var arch: any = py.get(repo, "architecture", {});
  return {"classification": arch, "topology": py.get(repo, "topology", {}), "runtime_graph": py.get(repo, "runtime_graph", {}), "deployment": py.get(repo, "deployment", {}), "evidence": "parser_backed_reconstruction"};
}
export { reconstructRepository };
