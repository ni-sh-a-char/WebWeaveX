/**
 * Converted from Python: core/extract/facades/internet_facade.py
 * @generated — WebWeaveX python→javascript library port
 */

import { canonicalizeSources, computeFreshness, computeTrust, prioritizeSources, rankSources, resolveDuplicates, semanticDedup } from "../../internet/index.js";
import { canonicalizeSourceSet, mergeSemanticSources, rankCrawlPriority, rankExtractionResults, resolveDuplicateSources, scoreFreshness, scoreRepositoryAuthority, scoreTrust, semanticSimilarity } from "../../internet/intelligence/index.js";
import { parseAdaptive } from "../../universal/adaptiveParserEngine.js";
import { detectBinaryBoundary } from "../../universal/binaryBoundaryEngine.js";
import { routeFormat } from "../../universal/formatRouterEngine.js";
import { parseSemanticPayload } from "../../universal/semanticPayloadEngine.js";
import { parseStructuredPayload as parseStructuredPayloadV3 } from "../../universal/structuredPayloadV3Engine.js";
import { parseUniversalPayload } from "../../universal/universalParserEngine.js";
import { extractBinaryMetadata } from "../../universal/binaryMetadataEngine.js";
import { extractArchiveIntelligence } from "../../universal/archiveIntelligenceEngine.js";
import { extractPackageIntelligence } from "../../universal/packageIntelligenceEngine.js";
import { extractApiSurfaceV2 } from "../../universal/apiSurfaceEngine.js";
import { detectProtocolIntelligence } from "../../universal/protocolIntelligenceEngine.js";
import { extractMediaStructure } from "../../universal/mediaStructureEngine.js";
import { extractStructuredPayload } from "../../universal/structuredPayloadEngine.js";
import { inspectArchive as inspectArchiveV4 } from "../../universal/archiveInspectionEngine.js";
import { inspectBinaryBoundary as inspectBinaryBoundaryV4 } from "../../universal/binaryBoundaryV4Engine.js";
import { parseCicd as parseCicdV4 } from "../../universal/cicdEngine.js";
import { parseGraphql } from "../../universal/graphqlEngine.js";
import { parseInfra as parseInfraV4 } from "../../universal/infraEngine.js";
import { parseNotebook } from "../../universal/notebookEngine.js";
import { parseOpenapi } from "../../universal/openapiEngine.js";
import { parseProtobuf } from "../../universal/protobufEngine.js";

export { canonicalizeSourceSet, canonicalizeSources, computeFreshness, computeTrust, detectBinaryBoundary, detectProtocolIntelligence, extractApiSurfaceV2, extractArchiveIntelligence, extractBinaryMetadata, extractMediaStructure, extractPackageIntelligence, extractStructuredPayload, inspectArchiveV4, inspectBinaryBoundaryV4, mergeSemanticSources, parseAdaptive, parseCicdV4, parseGraphql, parseInfraV4, parseNotebook, parseOpenapi, parseProtobuf, parseSemanticPayload, parseStructuredPayloadV3, parseUniversalPayload, prioritizeSources, rankCrawlPriority, rankExtractionResults, rankSources, resolveDuplicateSources, resolveDuplicates, routeFormat, scoreFreshness, scoreRepositoryAuthority, scoreTrust, semanticDedup, semanticSimilarity };
