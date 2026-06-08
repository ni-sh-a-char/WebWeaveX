/**
 * Barrel converted from core/internet/intelligence/__init__.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { canonicalizeSources as canonicalizeSourceSet, computeFreshness as scoreFreshness, computeTrust as scoreTrust, mergeSources as mergeSemanticSources, prioritizeSources as rankCrawlPriority, resolveDuplicates as resolveDuplicateSources, semanticSimilarity } from "../index.js";
import { rankByAuthority } from "../authorityEngine.js";
import { rankExtractions as rankExtractionResults } from "../extractionRankingEngine.js";
export { canonicalizeSourceSet, scoreFreshness, scoreTrust, mergeSemanticSources, rankCrawlPriority, resolveDuplicateSources, semanticSimilarity };
export { rankByAuthority };
export { rankExtractionResults };
export const scoreRepositoryAuthority = (url: any) => (py.truthy(url) ? py.at(rankByAuthority([url]), 0) : {"authority_score": py.F(0.0)});
