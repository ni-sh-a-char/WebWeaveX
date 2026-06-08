/**
 * Converted from Python: core/extract/advanced/architecture_extractor_v2.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { analyzeRepository } from "../../repository/repositoryIntelligence.js";

export function extractArchitectureV2(text: any, source_url: any = ""): any {
  var repo: any = analyzeRepository(text, source_url);
  return py.get(repo, "architecture", {"layers": [], "components": [], "relationships": []});
}
export { analyzeRepository };
