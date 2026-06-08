/**
 * Converted from Python: core/extract/enrichment_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildExecutionGraph, computeConfidence, deterministicTrace, extractionDiagnostics, normalizeOutput, parseSource, performanceMetrics, scoreExtraction, scoreSemanticConfidence, scoreStructureQuality } from "./facades/coreFacade.js";
import { analyzeDocument, analyzeSemanticDocs, buildConceptDependencies, buildDocConceptGraphV18, buildDocSemanticFlowV18, buildReferenceGraph, buildSemanticChunks, buildSemanticRelationships, buildToc, chunkSemanticV18, extractApiContractDocs, extractApiContractsV18, extractArchitectureDocs, extractArchitectureSectionsV18, extractCitations, extractCodeBlocks, extractCodeContext, extractCrossRefs, extractDependencyReferencesV18, extractDiagramRefs, extractKnowledgeBlocks, extractMigrationGuidesV18, extractSemanticApiDocs, extractSemanticCodeReferences, extractSemanticDiagrams, extractSemanticExamples, extractSemanticOutline, extractSemanticOutlineV16, extractSemanticReferences, extractSemanticSections, extractSemanticSpecs, extractSemanticTables, extractSemanticTutorials, extractTables, extractTutorialFlow, reconstructTutorialV18, resolveDocReferencesV4, synthesizeKnowledge } from "./facades/documentFacade.js";
import { boundGraphMemory, buildSemanticGraphFromIds, compressGraphV18, graphClusterV18, graphDiffV18, graphMemoryBoundV18, graphPartitionV18, graphReasonV18, graphSearchV18, graphSimilarityV18, graphTraverseV18, reasonTopology, scoreGraph, semanticPaths } from "./facades/graphFacade.js";
import { canonicalizeSourceSet, canonicalizeSources, computeFreshness, computeTrust, detectBinaryBoundary, detectProtocolIntelligence, extractApiSurfaceV2, extractArchiveIntelligence, extractBinaryMetadata, extractMediaStructure, extractPackageIntelligence, extractStructuredPayload, inspectArchiveV4, inspectBinaryBoundaryV4, mergeSemanticSources, parseAdaptive, parseCicdV4, parseGraphql, parseInfraV4, parseNotebook, parseOpenapi, parseProtobuf, parseSemanticPayload, parseStructuredPayloadV3, parseUniversalPayload, prioritizeSources, rankCrawlPriority, rankExtractionResults, rankSources, resolveDuplicateSources, resolveDuplicates, routeFormat, scoreFreshness, scoreRepositoryAuthority, scoreTrust, semanticDedup, semanticSimilarity } from "./facades/internetFacade.js";
import { buildArchitectureKnowledgeV18, buildArchitectureKnowledgeV2, buildConceptGraph, buildConceptGraphV18, buildDependencyKnowledgeV18, buildDependencyLineage, buildDocumentKnowledgeV2, buildDocumentationKnowledgeV18, buildExecutionFlow, buildFrameworkRelationships, buildInternetKnowledgeV2, buildKnowledgeRelationshipsV2, buildRepositoryKnowledge, buildRepositoryKnowledgeV18, buildRepositoryKnowledgeV2, buildSemanticGraph, buildSemanticIdentity, buildServiceRelationships, clusterSemanticGraph, reasonOverSemanticGraph, resolveEntities, resolveEntitiesV18 } from "./facades/knowledgeFacade.js";
import { buildCallGraph, buildDeploymentGraph, buildDistributedGraph, buildEventGraph, buildRepoDependencyLineageV18, buildRuntimeGraph, buildSemanticCallGraph, buildSemanticImportGraph, buildSemanticRepositoryGraph, buildSymbolGraph, classifyArchitectureV18, detectBuildSystems, detectFrameworks, detectLanguages, detectLocks, detectMonorepo, detectSemanticFrameworks, detectSemanticRuntime, extractApiContract, extractCiCd, extractRepositoryAst, extractSemanticAst, extractSemanticDependencies, extractSemanticRepository, inferEventTopology, inferOwnership, inferOwnershipDomains, inferRuntimeTopology, inferSemanticBuildGraph, inferSemanticServices, inferServiceBoundaries, mapInfrastructure, reconstructArchitecture, reconstructDomainModel, reconstructMonorepoV18, reconstructSemanticApi, reconstructSemanticArchitecture, reconstructTopology, resolveSemanticSymbols, summarizeRepository, traverseRepo } from "./facades/repositoryFacade.js";
import { budgetedChunks, decompressionGuard, enforceResourceBudget, incrementalParse, isSafeRemoteTarget, lazyExtract, malformedPayloadGuard, memoryBudget, memoryGuard, parserPool, recursionGuard, redirectGuard, sandboxText, ssrfGuard, streamParse, timeoutGuard } from "./facades/securityFacade.js";
import { dumpsDeterministic, fingerprintV3 } from "./facades/serializerFacade.js";

export function _merge(...parts: any[]): any {
  var out: Record<string, any> = {};
  var part: any;
  for (part of py.iter(parts)) {
    var key: any;
    var value: any;
    for ([key, value] of py.items(part)) {
      if (!py.contains(out, key)) {
        py.setItem(out, key, value);
      } else if ((((py.at(out, key) !== null && typeof py.at(out, key) === "object" && !Array.isArray(py.at(out, key)) && !(py.at(out, key) instanceof Set) && !(py.at(out, key) instanceof Map))) && ((value !== null && typeof value === "object" && !Array.isArray(value) && !(value instanceof Set) && !(value instanceof Map))))) {
        py.setItem(out, key, {...(py.at(out, key)), ...(value)});
      }
    }
  }
  return out;
}
export function enrichExtraction(normalized: any, safe_text: any, source_url: any, merged: any): any {
  py.setItem(py.at(normalized, "metadata"), "confidence", computeConfidence(normalized));
  py.setItem(py.at(normalized, "metadata"), "source", py.or2(source_url, () => ("raw")));
  py.setdefault(normalized, "metadata", {});
  py.setdefault(py.at(normalized, "metadata"), "llm", {});
  py.setdefault(py.at(normalized, "metadata"), "crawl", {});
  py.setdefault(py.at(normalized, "metadata"), "streaming", {});
  var repo: any = py.get(py.get(merged, "content", {}), "repository_intelligence_v12", {});
  var dep_nodes: any = py.get(py.get(repo, "dependency_graph", {}), "nodes", []);
  var dep_edges: any = py.get(py.get(repo, "dependency_graph", {}), "edges", []);
  var imp_edges: any = py.get(py.get(repo, "import_graph", {}), "edges", []);
  var api_routes: any = py.get(py.get(repo, "api_surface", {}), "routes", []);
  var refs: any = py.get(py.get(py.get(py.get(merged, "content", {}), "document_intelligence_v12", {}), "references", {}), "external_links", []);
  var route_edges: any = py.iter(py.slice(api_routes, null, 100)).map((r: any) => ({"from": "routes", "to": r}));
  var ref_edges: any = py.iter(py.slice(refs, null, 100)).map((r: any) => ({"from": "document", "to": r}));
  var graph: any = buildExecutionGraph({"nodes": dep_nodes, "edges": py.add(py.add(py.add(dep_edges, imp_edges), route_edges), ref_edges)});
  py.setItem(py.at(normalized, "relationships"), "execution_graph", graph);
  py.setItem(py.at(normalized, "relationships"), "reference_graph", buildReferenceGraph(safe_text));
  py.setItem(py.at(normalized, "content"), "repository", {"traversal": traverseRepo(safe_text), "monorepo": detectMonorepo(safe_text), "ci_cd": extractCiCd(safe_text), "services": py.get(py.get(repo, "topology", {}), "services", [])});
  var ast_data: any = extractRepositoryAst(safe_text);
  var frameworks: any = detectFrameworks(py.get(ast_data, "imports", []), py.get(py.get(normalized, "dependencies", {}), "packages", []));
  var arch: any = reconstructArchitecture(py.get(repo, "topology", {}), py.get(ast_data, "imports", []), py.get(py.get(repo, "api_surface", {}), "routes", []), py.get(py.get(normalized, "dependencies", {}), "packages", []));
  var api_contract: any = extractApiContract(py.get(repo, "api_surface", {}));
  var repo_parts: any = {"languages": detectLanguages(safe_text), "frameworks": frameworks, "ast": ast_data, "symbol_graph": buildSymbolGraph(ast_data), "call_graph": buildCallGraph(safe_text), "architecture": arch, "api_contract": api_contract, "build_systems": detectBuildSystems(safe_text), "package_locks": detectLocks(safe_text)};
  py.setItem(repo_parts, "summary", summarizeRepository(repo_parts));
  py.setItem(py.at(py.at(normalized, "content"), "repository"), "intelligence_v2", repo_parts);
  var semantic_ast: any = extractSemanticAst(safe_text);
  var semantic_symbols: any = resolveSemanticSymbols(semantic_ast);
  var semantic_dep: any = extractSemanticDependencies(safe_text);
  var semantic_api: any = reconstructSemanticApi(safe_text);
  var semantic_services: any = inferSemanticServices(py.get(repo, "topology", {}), py.get(semantic_ast, "imports", []), py.get(semantic_api, "routes", []), py.get(semantic_dep, "dependencies", []));
  var semantic_frameworks: any = detectSemanticFrameworks(py.get(semantic_ast, "imports", []), py.get(semantic_dep, "dependencies", []), py.get(repo_parts, "build_systems", []));
  var semantic_runtime: any = detectSemanticRuntime(py.get(semantic_dep, "dependencies", []), py.get(repo_parts, "build_systems", []), py.get(repo_parts, "package_locks", []));
  var semantic_arch: any = reconstructSemanticArchitecture(semantic_services, py.get(semantic_dep, "dependencies", []), py.get(semantic_ast, "imports", []), py.get(semantic_api, "routes", []));
  var semantic_build: any = inferSemanticBuildGraph(py.get(semantic_dep, "package_managers", []));
  var semantic_call: any = buildSemanticCallGraph(safe_text);
  var semantic_import_graph: any = buildSemanticImportGraph(semantic_ast, "repository");
  var semantic_repo_graph: any = buildSemanticRepositoryGraph({"symbols": py.get(semantic_symbols, "symbols", []), "frameworks": semantic_frameworks, "dependencies": py.get(semantic_dep, "dependencies", []), "services": py.get(semantic_services, "services", []), "routes": py.get(semantic_api, "routes", [])});
  py.setItem(py.at(py.at(normalized, "content"), "repository"), "semantic_v16", {"ast": semantic_ast, "symbols": semantic_symbols, "imports": semantic_import_graph, "calls": semantic_call, "dependencies": semantic_dep, "services": semantic_services, "runtime": semantic_runtime, "api": semantic_api, "build": semantic_build, "frameworks": semantic_frameworks, "architecture": semantic_arch, "repository_graph": semantic_repo_graph});
  var doc_base: any = analyzeDocument(safe_text);
  var doc_intel: any = {"semantic_outline": extractSemanticOutline(safe_text), "toc": buildToc(safe_text), "citations": extractCitations(safe_text), "knowledge_blocks": extractKnowledgeBlocks(safe_text), "code_blocks": extractCodeBlocks(safe_text), "tables": extractTables(safe_text), "diagram_references": extractDiagramRefs(safe_text), "cross_references": extractCrossRefs(safe_text)};
  var doc_semantic_v16: any = {"docs": analyzeSemanticDocs(safe_text), "references": extractSemanticReferences(safe_text), "api_docs": extractSemanticApiDocs(safe_text), "specs": extractSemanticSpecs(safe_text), "tutorials": extractSemanticTutorials(safe_text), "outline": extractSemanticOutlineV16(safe_text), "examples": extractSemanticExamples(safe_text), "code_references": extractSemanticCodeReferences(safe_text), "diagrams": extractSemanticDiagrams(safe_text), "tables": extractSemanticTables(safe_text)};
  py.setItem(doc_semantic_v16, "relationships", buildSemanticRelationships(py.iter(py.get(py.at(doc_semantic_v16, "outline"), "headings", [])).map((h: any) => py.get(h, "title", "")), py.get(py.at(doc_semantic_v16, "references"), "external", [])));
  py.setItem(py.at(normalized, "content"), "documents", {"base": doc_base, "intelligence_v2": doc_intel, "semantic_v16": doc_semantic_v16});
  var repo_knowledge_graph: any = buildRepositoryKnowledge({"symbols": py.get(semantic_symbols, "symbols", []), "dependencies": py.get(semantic_dep, "dependencies", []), "frameworks": semantic_frameworks, "services": py.get(semantic_services, "services", [])});
  var service_graph: any = buildServiceRelationships(py.get(semantic_services, "services", []));
  var dependency_lineage: any = buildDependencyLineage(py.get(semantic_dep, "dependencies", []));
  var framework_graph: any = buildFrameworkRelationships(semantic_frameworks, py.get(semantic_services, "services", []));
  var execution_flow: any = buildExecutionFlow(py.get(semantic_call, "calls", []));
  var semantic_graph: any = buildSemanticGraph({"nodes": py.add(py.get(repo_knowledge_graph, "nodes", []), py.get(framework_graph, "nodes", [])), "edges": py.add(py.add(py.get(repo_knowledge_graph, "edges", []), py.get(framework_graph, "edges", [])), py.get(execution_flow, "edges", []))});
  py.setItem(py.at(normalized, "content"), "knowledge", {"repository_knowledge_graph": repo_knowledge_graph, "service_relationships": service_graph, "dependency_lineage": dependency_lineage, "framework_relationships": framework_graph, "execution_flow": execution_flow, "semantic_clusters": clusterSemanticGraph(semantic_graph), "semantic_graph": semantic_graph, "reasoning": reasonOverSemanticGraph(semantic_graph)});
  py.setItem(py.at(normalized, "content"), "universal_v16", {"parser": parseUniversalPayload(safe_text, source_url), "binary_metadata": extractBinaryMetadata(safe_text), "archive_intelligence": extractArchiveIntelligence(py.or2(source_url, () => (py.slice(safe_text, null, 200)))), "package_intelligence": extractPackageIntelligence(safe_text), "api_surface": extractApiSurfaceV2(safe_text), "protocol_intelligence": detectProtocolIntelligence(source_url), "media_structure": extractMediaStructure(safe_text), "structured_payload": extractStructuredPayload(safe_text)});
  var repository_v17: any = extractSemanticRepository(safe_text, source_url);
  var arch_v2: any = {"service_boundaries": inferServiceBoundaries(py.get(py.get(repository_v17, "symbols", {}), "symbols", [])), "event_topology": inferEventTopology(safe_text), "runtime_topology": inferRuntimeTopology(py.get(py.get(repository_v17, "dependencies", {}), "dependencies", [])), "distributed_graph": buildDistributedGraph(py.get(py.get(repository_v17, "services", {}), "services", []), py.get(py.get(repository_v17, "dependencies", {}), "dependencies", [])), "domain_model": reconstructDomainModel(py.get(py.get(repository_v17, "symbols", {}), "symbols", [])), "ownership": inferOwnership(py.get(py.get(repository_v17, "symbols", {}), "symbols", [])), "infrastructure": mapInfrastructure(safe_text)};
  py.setItem(py.at(py.at(normalized, "content"), "repository"), "semantic_v17", repository_v17);
  py.setItem(py.at(py.at(normalized, "content"), "repository"), "architecture_v2", arch_v2);
  var docs_v4: any = {"sections": extractSemanticSections(safe_text), "tutorial_flow": extractTutorialFlow(safe_text), "concept_dependencies": buildConceptDependencies(safe_text), "references": resolveDocReferencesV4(safe_text), "chunks": buildSemanticChunks(safe_text), "code_context": extractCodeContext(safe_text), "architecture_docs": extractArchitectureDocs(safe_text), "api_contract_docs": extractApiContractDocs(safe_text)};
  py.setItem(docs_v4, "knowledge", synthesizeKnowledge(docs_v4));
  py.setItem(py.at(py.at(normalized, "content"), "documents"), "intelligence_v4", docs_v4);
  var internet_urls: any = py.iter(py.add([source_url], refs)).filter((u: any) => py.truthy(u)).map((u: any) => u);
  var canonical_urls: any = canonicalizeSources(internet_urls);
  py.setItem(py.at(normalized, "content"), "internet", {"canonical_sources": canonical_urls, "ranked_sources": rankSources(canonical_urls), "priority_sources": prioritizeSources(canonical_urls), "dedup_text": semanticDedup([safe_text]), "freshness": computeFreshness({"source_count": py.len(canonical_urls)}), "trust": computeTrust(source_url), "duplicates_removed": resolveDuplicates(py.iter(canonical_urls).map((u: any) => ({"url": u})))});
  var fmt: any = routeFormat(py.get(py.get(py.get(normalized, "metadata", {}), "fetch", {}), "content_type", ""), source_url);
  py.setItem(py.at(normalized, "content"), "universal_v17", {"format": fmt, "adaptive": parseAdaptive(safe_text, fmt), "binary_boundary": detectBinaryBoundary(safe_text), "structured_payload": parseStructuredPayloadV3(safe_text), "semantic_payload": parseSemanticPayload(safe_text)});
  var exec_graph: any = py.get(py.get(normalized, "relationships", {}), "execution_graph", {});
  var nodes_v7: any = py.iter(py.get(exec_graph, "nodes", [])).map((n: any) => (((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map))) ? py.get(n, "id", "") : py.toStr(n)));
  var graph_v7: any = buildSemanticGraphFromIds(nodes_v7, py.get(exec_graph, "edges", []));
  graph_v7 = boundGraphMemory(graph_v7);
  py.setItem(py.at(normalized, "relationships"), "execution_graph_v7", graph_v7);
  py.setItem(py.at(normalized, "metadata"), "graph_v7", {"reasoning": reasonTopology(graph_v7), "score": scoreGraph(graph_v7)});
  var knowledge_v2: any = {"entities": resolveEntities(py.get(py.get(repository_v17, "symbols", {}), "symbols", [])), "concept_graph": buildConceptGraph(py.get(py.get(repository_v17, "symbols", {}), "symbols", [])), "semantic_relationships": buildKnowledgeRelationshipsV2(py.get(py.get(repository_v17, "symbols", {}), "symbols", []), py.get(py.get(repository_v17, "dependencies", {}), "dependencies", [])), "repository_knowledge": buildRepositoryKnowledgeV2({"symbols": py.get(py.get(repository_v17, "symbols", {}), "symbols", []), "dependencies": py.get(py.get(repository_v17, "dependencies", {}), "dependencies", []), "frameworks": py.get(repository_v17, "frameworks", [])}), "document_knowledge": buildDocumentKnowledgeV2(docs_v4), "internet_knowledge": buildInternetKnowledgeV2(canonical_urls), "architecture_knowledge": buildArchitectureKnowledgeV2(py.get(repository_v17, "architecture", {}))};
  py.setItem(py.at(normalized, "content"), "knowledge_v2", knowledge_v2);
  py.setItem(py.at(normalized, "metadata"), "quality_v17", {"extraction": scoreExtraction(normalized), "semantic": scoreSemanticConfidence(normalized), "structure": scoreStructureQuality(graph_v7)});
  py.setItem(py.at(normalized, "metadata"), "security_v17", {"safe_remote_target": (py.truthy(source_url) ? isSafeRemoteTarget(source_url) : true), "resource_budget": enforceResourceBudget(py.len(py.encode(safe_text, "utf-8")))});
  var parsed_v18: any = parseSource(safe_text, py.or2(source_url, () => ("input")));
  var symbols_v18: any = py.get(parsed_v18, "symbols", {});
  var repo_paths: any = py.get(py.get(py.get(py.get(normalized, "content", {}), "repository", {}), "traversal", {}), "paths", []);
  var topo_v18: any = reconstructTopology(((Array.isArray(repo_paths)) ? repo_paths : []));
  var event_v18: any = buildEventGraph(safe_text);
  var runtime_v18: any = buildRuntimeGraph(py.get(py.get(parsed_v18, "runtime", {}), "runtimes", []), py.get(topo_v18, "services", []));
  var deploy_v18: any = buildDeploymentGraph(safe_text);
  var arch_class_v18: any = classifyArchitectureV18(topo_v18, event_v18, deploy_v18);
  var monorepo_v18: any = reconstructMonorepoV18(((Array.isArray(repo_paths)) ? repo_paths : []));
  var ownership_v18: any = inferOwnershipDomains(((Array.isArray(repo_paths)) ? repo_paths : []));
  var dep_lineage_v18: any = buildRepoDependencyLineageV18(py.get(py.get(parsed_v18, "dependencies", {}), "dependencies", []));
  py.setItem(py.at(py.at(normalized, "content"), "repository"), "reconstruction_v18", {"topology": topo_v18, "events": event_v18, "runtime_graph": runtime_v18, "deployment": deploy_v18, "architecture_classification": arch_class_v18, "monorepo": monorepo_v18, "ownership": ownership_v18, "dependency_lineage": dep_lineage_v18, "parser": parsed_v18});
  var doc_v18: any = {"semantic_flow": buildDocSemanticFlowV18(safe_text), "tutorial": reconstructTutorialV18(safe_text), "concept_graph": buildDocConceptGraphV18(safe_text), "chunks": chunkSemanticV18(safe_text), "api_contracts": extractApiContractsV18(safe_text), "architecture_docs": extractArchitectureSectionsV18(safe_text), "dependency_references": extractDependencyReferencesV18(safe_text), "migration": extractMigrationGuidesV18(safe_text)};
  py.setItem(py.at(py.at(normalized, "content"), "documents"), "reconstruction_v18", doc_v18);
  var canonical_sources_v18: any = canonicalizeSourceSet(py.iter(py.add([source_url], refs)).filter((u: any) => py.truthy(u)).map((u: any) => u));
  var internet_v18: any = {"sources": canonical_sources_v18, "trust": scoreTrust(source_url), "freshness": scoreFreshness({"sources": py.len(canonical_sources_v18)}), "dedup_sources": resolveDuplicateSources(py.iter(canonical_sources_v18).map((u: any) => ({"url": u}))), "source_merge": mergeSemanticSources([{"source_url": source_url, "text_len": py.len(safe_text)}]), "crawl_priority": rankCrawlPriority(canonical_sources_v18), "repository_authority": scoreRepositoryAuthority(source_url)};
  if ((py.len(canonical_sources_v18) >= 2)) {
    py.setItem(internet_v18, "semantic_similarity", semanticSimilarity(py.at(canonical_sources_v18, 0), py.at(canonical_sources_v18, 1)));
  } else {
    py.setItem(internet_v18, "semantic_similarity", {"score": py.F(1.0)});
  }
  py.setItem(py.at(py.at(normalized, "content"), "internet"), "intelligence_v18", internet_v18);
  var universal_v18: any = {"openapi": parseOpenapi(safe_text), "graphql": parseGraphql(safe_text), "protobuf": parseProtobuf(safe_text), "notebook": parseNotebook(safe_text), "archive": inspectArchiveV4(py.or2(source_url, () => (py.slice(safe_text, null, 256)))), "cicd": parseCicdV4(safe_text), "infra": parseInfraV4(safe_text), "binary_boundary": inspectBinaryBoundaryV4(safe_text)};
  py.setItem(py.at(normalized, "content"), "universal_v18", universal_v18);
  var graph_base_v18: any = py.get(py.get(normalized, "relationships", {}), "execution_graph_v7", py.get(py.get(normalized, "relationships", {}), "execution_graph", {}));
  var graph_bounded_v18: any = graphMemoryBoundV18(graph_base_v18);
  var graph_reasoned_v18: any = {"reasoning": graphReasonV18(graph_bounded_v18), "clusters": graphClusterV18(graph_bounded_v18), "partitions": graphPartitionV18(graph_bounded_v18), "search_document": graphSearchV18(graph_bounded_v18, "document"), "paths_document": semanticPaths(graph_bounded_v18, "document", 3), "traversal_document": graphTraverseV18(graph_bounded_v18, "document"), "self_similarity": graphSimilarityV18(graph_bounded_v18, graph_bounded_v18), "self_diff": graphDiffV18(graph_bounded_v18, graph_bounded_v18)};
  py.setItem(py.at(normalized, "relationships"), "graph_reasoning_v18", graph_reasoned_v18);
  py.setItem(py.at(normalized, "relationships"), "execution_graph_v18", compressGraphV18(graph_bounded_v18));
  var knowledge_v18: any = {"entities": resolveEntitiesV18(py.get(symbols_v18, "symbols", [])), "identity": buildSemanticIdentity(py.or2(source_url, () => ("input"))), "concept_graph": buildConceptGraphV18(py.get(symbols_v18, "symbols", [])), "repository_knowledge": buildRepositoryKnowledgeV18({"symbols": py.get(symbols_v18, "symbols", []), "dependencies": py.get(py.get(parsed_v18, "dependencies", {}), "dependencies", []), "frameworks": py.get(py.get(py.get(py.get(normalized, "content", {}), "repository", {}), "semantic_v17", {}), "frameworks", [])}), "documentation_knowledge": buildDocumentationKnowledgeV18({"sections": ((Array.isArray(py.get(py.get(doc_v18, "semantic_flow", {}), "nodes", []))) ? py.iter(py.get(py.get(doc_v18, "semantic_flow", {}), "nodes", [])).map((s: any) => py.toStr(s)) : []), "references": py.get(py.get(doc_v18, "api_contracts", {}), "routes", [])}), "architecture_knowledge": buildArchitectureKnowledgeV18({"styles": py.get(arch_class_v18, "styles", []), "relationships": py.get(event_v18, "edges", [])}), "dependency_knowledge": buildDependencyKnowledgeV18(py.get(py.get(parsed_v18, "dependencies", {}), "dependencies", []))};
  py.setItem(py.at(normalized, "content"), "knowledge_reconstruction_v18", knowledge_v18);
  py.setItem(py.at(normalized, "metadata"), "quality_v18", {"ranked_extractions": py.iter(rankExtractionResults([normalized])).map((r: any) => ({"source_url": py.get(r, "source_url", ""), "raw_text_len": py.len(py.or2(py.get(r, "raw_text", ""), () => (""))), "edge_count": py.len(py.get(py.get(py.get(r, "relationships", {}), "execution_graph", {}), "edges", []))})), "structure_score": scoreStructureQuality(graph_bounded_v18)});
  py.setItem(py.at(normalized, "metadata"), "security_v18", {"ssrf": (py.truthy(source_url) ? ssrfGuard(source_url) : {"ok": true}), "redirect": redirectGuard((py.truthy(source_url) ? [source_url] : [])), "malformed_payload": malformedPayloadGuard(safe_text), "recursion": recursionGuard(0), "memory": memoryGuard(py.len(py.encode(safe_text, "utf-8"))), "decompression": decompressionGuard(1, py.len(py.encode(safe_text, "utf-8")))});
  py.setItem(py.at(normalized, "metadata"), "performance_v18", {"parser_pool": parserPool(), "stream_chunks": py.len(streamParse(safe_text)), "incremental_segments": py.len(py.get(incrementalParse(safe_text), "segments", [])), "budgeted_chunks": py.len(budgetedChunks(safe_text)), "memory_budget": memoryBudget(py.len(py.encode(safe_text, "utf-8"))), "timeout": timeoutGuard(py.F(0.0)), "lazy_preview": lazyExtract(safe_text, ["length", "preview"])});
  py.setItem(py.at(normalized, "metadata"), "observability_v18", {"diagnostics": extractionDiagnostics(normalized), "metrics": performanceMetrics({"extract_ms": py.F(0.0)}), "trace": deterministicTrace(py.or2(source_url, () => ("input")))});
  var canonical: any = dumpsDeterministic(normalized);
  py.setItem(py.at(normalized, "metadata"), "serialization_v4", {"canonical_length": py.len(canonical)});
  py.setItem(py.at(normalized, "metadata"), "serialization_v5", {"canonical_length": py.len(canonical)});
  py.setItem(normalized, "fingerprint", fingerprintV3(normalized));
  return normalized;
}
export { analyzeDocument, analyzeSemanticDocs, boundGraphMemory, budgetedChunks, buildArchitectureKnowledgeV18, buildArchitectureKnowledgeV2, buildCallGraph, buildConceptDependencies, buildConceptGraph, buildConceptGraphV18, buildDependencyKnowledgeV18, buildDependencyLineage, buildDeploymentGraph, buildDistributedGraph, buildDocConceptGraphV18, buildDocSemanticFlowV18, buildDocumentKnowledgeV2, buildDocumentationKnowledgeV18, buildEventGraph, buildExecutionFlow, buildExecutionGraph, buildFrameworkRelationships, buildInternetKnowledgeV2, buildKnowledgeRelationshipsV2, buildReferenceGraph, buildRepoDependencyLineageV18, buildRepositoryKnowledge, buildRepositoryKnowledgeV18, buildRepositoryKnowledgeV2, buildRuntimeGraph, buildSemanticCallGraph, buildSemanticChunks, buildSemanticGraph, buildSemanticGraphFromIds, buildSemanticIdentity, buildSemanticImportGraph, buildSemanticRelationships, buildSemanticRepositoryGraph, buildServiceRelationships, buildSymbolGraph, buildToc, canonicalizeSourceSet, canonicalizeSources, chunkSemanticV18, classifyArchitectureV18, clusterSemanticGraph, compressGraphV18, computeConfidence, computeFreshness, computeTrust, decompressionGuard, detectBinaryBoundary, detectBuildSystems, detectFrameworks, detectLanguages, detectLocks, detectMonorepo, detectProtocolIntelligence, detectSemanticFrameworks, detectSemanticRuntime, deterministicTrace, dumpsDeterministic, enforceResourceBudget, extractApiContract, extractApiContractDocs, extractApiContractsV18, extractApiSurfaceV2, extractArchitectureDocs, extractArchitectureSectionsV18, extractArchiveIntelligence, extractBinaryMetadata, extractCiCd, extractCitations, extractCodeBlocks, extractCodeContext, extractCrossRefs, extractDependencyReferencesV18, extractDiagramRefs, extractKnowledgeBlocks, extractMediaStructure, extractMigrationGuidesV18, extractPackageIntelligence, extractRepositoryAst, extractSemanticApiDocs, extractSemanticAst, extractSemanticCodeReferences, extractSemanticDependencies, extractSemanticDiagrams, extractSemanticExamples, extractSemanticOutline, extractSemanticOutlineV16, extractSemanticReferences, extractSemanticRepository, extractSemanticSections, extractSemanticSpecs, extractSemanticTables, extractSemanticTutorials, extractStructuredPayload, extractTables, extractTutorialFlow, extractionDiagnostics, fingerprintV3, graphClusterV18, graphDiffV18, graphMemoryBoundV18, graphPartitionV18, graphReasonV18, graphSearchV18, graphSimilarityV18, graphTraverseV18, incrementalParse, inferEventTopology, inferOwnership, inferOwnershipDomains, inferRuntimeTopology, inferSemanticBuildGraph, inferSemanticServices, inferServiceBoundaries, inspectArchiveV4, inspectBinaryBoundaryV4, isSafeRemoteTarget, lazyExtract, malformedPayloadGuard, mapInfrastructure, memoryBudget, memoryGuard, mergeSemanticSources, normalizeOutput, parseAdaptive, parseCicdV4, parseGraphql, parseInfraV4, parseNotebook, parseOpenapi, parseProtobuf, parseSemanticPayload, parseSource, parseStructuredPayloadV3, parseUniversalPayload, parserPool, performanceMetrics, prioritizeSources, rankCrawlPriority, rankExtractionResults, rankSources, reasonOverSemanticGraph, reasonTopology, reconstructArchitecture, reconstructDomainModel, reconstructMonorepoV18, reconstructSemanticApi, reconstructSemanticArchitecture, reconstructTopology, reconstructTutorialV18, recursionGuard, redirectGuard, resolveDocReferencesV4, resolveDuplicateSources, resolveDuplicates, resolveEntities, resolveEntitiesV18, resolveSemanticSymbols, routeFormat, sandboxText, scoreExtraction, scoreFreshness, scoreGraph, scoreRepositoryAuthority, scoreSemanticConfidence, scoreStructureQuality, scoreTrust, semanticDedup, semanticPaths, semanticSimilarity, ssrfGuard, streamParse, summarizeRepository, synthesizeKnowledge, timeoutGuard, traverseRepo };
