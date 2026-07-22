from __future__ import annotations

from typing import Any, Dict

from core.extract.facades.core_facade import *  # noqa: F403
from core.extract.facades.document_facade import *  # noqa: F403
from core.extract.facades.graph_facade import *  # noqa: F403
from core.extract.facades.internet_facade import *  # noqa: F403
from core.extract.facades.knowledge_facade import *  # noqa: F403
from core.extract.facades.repository_facade import *  # noqa: F403
from core.extract.facades.security_facade import *  # noqa: F403
from core.serialize.deterministic_serializer import dumps_deterministic
from core.crypto import fingerprint_v3
from core.extract.facades.parser_facade import parse_source


def _merge(*parts: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for part in parts:
        for key, value in part.items():
            if key not in out:
                out[key] = value
            elif isinstance(out[key], dict) and isinstance(value, dict):
                out[key] = {**out[key], **value}
    return out


def enrich_extraction(
    normalized: Dict[str, Any],
    safe_text: str,
    source_url: str,
    merged: Dict[str, Any],
) -> Dict[str, Any]:
    normalized["metadata"]["confidence"] = compute_confidence(normalized)
    normalized["metadata"]["source"] = source_url or "raw"
    normalized.setdefault("metadata", {})
    normalized["metadata"].setdefault("llm", {})
    normalized["metadata"].setdefault("crawl", {})
    normalized["metadata"].setdefault("streaming", {})

    repo = merged.get("content", {}).get("repository_intelligence_v12", {})
    dep_nodes = repo.get("dependency_graph", {}).get("nodes", [])
    dep_edges = repo.get("dependency_graph", {}).get("edges", [])
    imp_edges = repo.get("import_graph", {}).get("edges", [])
    api_routes = repo.get("api_surface", {}).get("routes", [])
    refs = merged.get("content", {}).get("document_intelligence_v12", {}).get("references", {}).get("external_links", [])
    route_edges = [{"from": "routes", "to": r} for r in api_routes[:100]]
    ref_edges = [{"from": "document", "to": r} for r in refs[:100]]
    graph = build_execution_graph({"nodes": dep_nodes, "edges": dep_edges + imp_edges + route_edges + ref_edges})
    normalized["relationships"]["execution_graph"] = graph
    normalized["relationships"]["reference_graph"] = build_reference_graph(safe_text)
    normalized["content"]["repository"] = {
        "traversal": traverse_repo(safe_text),
        "monorepo": detect_monorepo(safe_text),
        "ci_cd": extract_ci_cd(safe_text),
        "services": repo.get("topology", {}).get("services", []),
    }
    ast_data = extract_repository_ast(safe_text)
    frameworks = detect_frameworks(ast_data.get("imports", []), normalized.get("dependencies", {}).get("packages", []))
    arch = reconstruct_architecture(
        repo.get("topology", {}),
        ast_data.get("imports", []),
        repo.get("api_surface", {}).get("routes", []),
        normalized.get("dependencies", {}).get("packages", []),
    )
    api_contract = extract_api_contract(repo.get("api_surface", {}))
    repo_parts = {
        "languages": detect_languages(safe_text),
        "frameworks": frameworks,
        "ast": ast_data,
        "symbol_graph": build_symbol_graph(ast_data),
        "call_graph": build_call_graph(safe_text),
        "architecture": arch,
        "api_contract": api_contract,
        "build_systems": detect_build_systems(safe_text),
        "package_locks": detect_locks(safe_text),
    }
    repo_parts["summary"] = summarize_repository(repo_parts)
    normalized["content"]["repository"]["intelligence_v2"] = repo_parts

    semantic_ast = extract_semantic_ast(safe_text)
    semantic_symbols = resolve_semantic_symbols(semantic_ast)
    semantic_dep = extract_semantic_dependencies(safe_text)
    semantic_api = reconstruct_semantic_api(safe_text)
    semantic_services = infer_semantic_services(
        repo.get("topology", {}),
        semantic_ast.get("imports", []),
        semantic_api.get("routes", []),
        semantic_dep.get("dependencies", []),
    )
    semantic_frameworks = detect_semantic_frameworks(
        semantic_ast.get("imports", []),
        semantic_dep.get("dependencies", []),
        repo_parts.get("build_systems", []),
    )
    semantic_runtime = detect_semantic_runtime(
        semantic_dep.get("dependencies", []),
        repo_parts.get("build_systems", []),
        repo_parts.get("package_locks", []),
    )
    semantic_arch = reconstruct_semantic_architecture(
        semantic_services,
        semantic_dep.get("dependencies", []),
        semantic_ast.get("imports", []),
        semantic_api.get("routes", []),
    )
    semantic_build = infer_semantic_build_graph(semantic_dep.get("package_managers", []))
    semantic_call = build_semantic_call_graph(safe_text)
    semantic_import_graph = build_semantic_import_graph(semantic_ast, source="repository")
    semantic_repo_graph = build_semantic_repository_graph(
        {
            "symbols": semantic_symbols.get("symbols", []),
            "frameworks": semantic_frameworks,
            "dependencies": semantic_dep.get("dependencies", []),
            "services": semantic_services.get("services", []),
            "routes": semantic_api.get("routes", []),
        }
    )

    normalized["content"]["repository"]["semantic_v16"] = {
        "ast": semantic_ast,
        "symbols": semantic_symbols,
        "imports": semantic_import_graph,
        "calls": semantic_call,
        "dependencies": semantic_dep,
        "services": semantic_services,
        "runtime": semantic_runtime,
        "api": semantic_api,
        "build": semantic_build,
        "frameworks": semantic_frameworks,
        "architecture": semantic_arch,
        "repository_graph": semantic_repo_graph,
    }
    doc_base = analyze_document(safe_text)
    doc_intel = {
        "semantic_outline": extract_semantic_outline(safe_text),
        "toc": build_toc(safe_text),
        "citations": extract_citations(safe_text),
        "knowledge_blocks": extract_knowledge_blocks(safe_text),
        "code_blocks": extract_code_blocks(safe_text),
        "tables": extract_tables(safe_text),
        "diagram_references": extract_diagram_refs(safe_text),
        "cross_references": extract_cross_refs(safe_text),
    }
    doc_semantic_v16 = {
        "docs": analyze_semantic_docs(safe_text),
        "references": extract_semantic_references(safe_text),
        "api_docs": extract_semantic_api_docs(safe_text),
        "specs": extract_semantic_specs(safe_text),
        "tutorials": extract_semantic_tutorials(safe_text),
        "outline": extract_semantic_outline_v16(safe_text),
        "examples": extract_semantic_examples(safe_text),
        "code_references": extract_semantic_code_references(safe_text),
        "diagrams": extract_semantic_diagrams(safe_text),
        "tables": extract_semantic_tables(safe_text),
    }
    doc_semantic_v16["relationships"] = build_semantic_relationships(
        [h.get("title", "") for h in doc_semantic_v16["outline"].get("headings", [])],
        doc_semantic_v16["references"].get("external", []),
    )
    normalized["content"]["documents"] = {
        "base": doc_base,
        "intelligence_v2": doc_intel,
        "semantic_v16": doc_semantic_v16,
    }

    repo_knowledge_graph = build_repository_knowledge(
        {
            "symbols": semantic_symbols.get("symbols", []),
            "dependencies": semantic_dep.get("dependencies", []),
            "frameworks": semantic_frameworks,
            "services": semantic_services.get("services", []),
        }
    )
    service_graph = build_service_relationships(semantic_services.get("services", []))
    dependency_lineage = build_dependency_lineage(semantic_dep.get("dependencies", []))
    framework_graph = build_framework_relationships(semantic_frameworks, semantic_services.get("services", []))
    execution_flow = build_execution_flow(semantic_call.get("calls", []))
    semantic_graph = build_semantic_graph(
        {
            "nodes": repo_knowledge_graph.get("nodes", []) + framework_graph.get("nodes", []),
            "edges": repo_knowledge_graph.get("edges", []) + framework_graph.get("edges", []) + execution_flow.get("edges", []),
        }
    )
    normalized["content"]["knowledge"] = {
        "repository_knowledge_graph": repo_knowledge_graph,
        "service_relationships": service_graph,
        "dependency_lineage": dependency_lineage,
        "framework_relationships": framework_graph,
        "execution_flow": execution_flow,
        "semantic_clusters": cluster_semantic_graph(semantic_graph),
        "semantic_graph": semantic_graph,
        "reasoning": reason_over_semantic_graph(semantic_graph),
    }

    normalized["content"]["universal_v16"] = {
        "parser": parse_universal_payload(safe_text, source_url=source_url),
        "binary_metadata": extract_binary_metadata(safe_text),
        "archive_intelligence": extract_archive_intelligence(source_url or safe_text[:200]),
        "package_intelligence": extract_package_intelligence(safe_text),
        "api_surface": extract_api_surface_v2(safe_text),
        "protocol_intelligence": detect_protocol_intelligence(source_url),
        "media_structure": extract_media_structure(safe_text),
        "structured_payload": extract_structured_payload(safe_text),
    }

    repository_v17 = extract_semantic_repository(safe_text, source_url=source_url)
    arch_v2 = {
        "service_boundaries": infer_service_boundaries(repository_v17.get("symbols", {}).get("symbols", [])),
        "event_topology": infer_event_topology(safe_text),
        "runtime_topology": infer_runtime_topology(repository_v17.get("dependencies", {}).get("dependencies", [])),
        "distributed_graph": build_distributed_graph(
            repository_v17.get("services", {}).get("services", []),
            repository_v17.get("dependencies", {}).get("dependencies", []),
        ),
        "domain_model": reconstruct_domain_model(repository_v17.get("symbols", {}).get("symbols", [])),
        "ownership": infer_ownership(repository_v17.get("symbols", {}).get("symbols", [])),
        "infrastructure": map_infrastructure(safe_text),
    }
    normalized["content"]["repository"]["semantic_v17"] = repository_v17
    normalized["content"]["repository"]["architecture_v2"] = arch_v2

    docs_v4 = {
        "sections": extract_semantic_sections(safe_text),
        "tutorial_flow": extract_tutorial_flow(safe_text),
        "concept_dependencies": build_concept_dependencies(safe_text),
        "references": resolve_doc_references_v4(safe_text),
        "chunks": build_semantic_chunks(safe_text),
        "code_context": extract_code_context(safe_text),
        "architecture_docs": extract_architecture_docs(safe_text),
        "api_contract_docs": extract_api_contract_docs(safe_text),
    }
    docs_v4["knowledge"] = synthesize_knowledge(docs_v4)
    normalized["content"]["documents"]["intelligence_v4"] = docs_v4

    internet_urls = [u for u in [source_url] + refs if u]
    canonical_urls = canonicalize_sources(internet_urls)
    normalized["content"]["internet"] = {
        "canonical_sources": canonical_urls,
        "ranked_sources": rank_sources(canonical_urls),
        "priority_sources": prioritize_sources(canonical_urls),
        "dedup_text": semantic_dedup([safe_text]),
        "freshness": compute_freshness({"source_count": len(canonical_urls)}),
        "trust": compute_trust(source_url),
        "duplicates_removed": resolve_duplicates([{"url": u} for u in canonical_urls]),
    }

    fmt = route_format(normalized.get("metadata", {}).get("fetch", {}).get("content_type", ""), source_url=source_url)
    normalized["content"]["universal_v17"] = {
        "format": fmt,
        "adaptive": parse_adaptive(safe_text, fmt),
        "binary_boundary": detect_binary_boundary(safe_text),
        "structured_payload": parse_structured_payload_v3(safe_text),
        "semantic_payload": parse_semantic_payload(safe_text),
    }

    exec_graph = normalized.get("relationships", {}).get("execution_graph", {})
    nodes_v7 = [n.get("id", "") if isinstance(n, dict) else str(n) for n in exec_graph.get("nodes", [])]
    graph_v7 = build_semantic_graph_from_ids(nodes_v7, exec_graph.get("edges", []))
    graph_v7 = bound_graph_memory(graph_v7)
    normalized["relationships"]["execution_graph_v7"] = graph_v7
    normalized["metadata"]["graph_v7"] = {
        "reasoning": reason_topology(graph_v7),
        "score": score_graph(graph_v7),
    }

    knowledge_v2 = {
        "entities": resolve_entities(repository_v17.get("symbols", {}).get("symbols", [])),
        "concept_graph": build_concept_graph(repository_v17.get("symbols", {}).get("symbols", [])),
        "semantic_relationships": build_knowledge_relationships_v2(
            repository_v17.get("symbols", {}).get("symbols", []),
            repository_v17.get("dependencies", {}).get("dependencies", []),
        ),
        "repository_knowledge": build_repository_knowledge_v2(
            {
                "symbols": repository_v17.get("symbols", {}).get("symbols", []),
                "dependencies": repository_v17.get("dependencies", {}).get("dependencies", []),
                "frameworks": repository_v17.get("frameworks", []),
            }
        ),
        "document_knowledge": build_document_knowledge_v2(docs_v4),
        "internet_knowledge": build_internet_knowledge_v2(canonical_urls),
        "architecture_knowledge": build_architecture_knowledge_v2(repository_v17.get("architecture", {})),
    }
    normalized["content"]["knowledge_v2"] = knowledge_v2

    normalized["metadata"]["quality_v17"] = {
        "extraction": score_extraction(normalized),
        "semantic": score_semantic_confidence(normalized),
        "structure": score_structure_quality(graph_v7),
    }
    normalized["metadata"]["security_v17"] = {
        "safe_remote_target": is_safe_remote_target(source_url) if source_url else True,
        "resource_budget": enforce_resource_budget(len(safe_text.encode("utf-8", errors="ignore"))),
    }

    parsed_v18 = parse_source(safe_text, path=source_url or "input")
    symbols_v18 = parsed_v18.get("symbols", {})
    repo_paths = normalized.get("content", {}).get("repository", {}).get("traversal", {}).get("paths", [])
    topo_v18 = reconstruct_topology(repo_paths if isinstance(repo_paths, list) else [])
    event_v18 = build_event_graph(safe_text)
    runtime_v18 = build_runtime_graph(parsed_v18.get("runtime", {}).get("runtimes", []), topo_v18.get("services", []))
    deploy_v18 = build_deployment_graph(safe_text)
    arch_class_v18 = classify_architecture_v18(topo_v18, event_v18, deploy_v18)
    monorepo_v18 = reconstruct_monorepo_v18(repo_paths if isinstance(repo_paths, list) else [])
    ownership_v18 = infer_ownership_domains(repo_paths if isinstance(repo_paths, list) else [])
    dep_lineage_v18 = build_repo_dependency_lineage_v18(parsed_v18.get("dependencies", {}).get("dependencies", []))
    normalized["content"]["repository"]["reconstruction_v18"] = {
        "topology": topo_v18,
        "events": event_v18,
        "runtime_graph": runtime_v18,
        "deployment": deploy_v18,
        "architecture_classification": arch_class_v18,
        "monorepo": monorepo_v18,
        "ownership": ownership_v18,
        "dependency_lineage": dep_lineage_v18,
        "parser": parsed_v18,
    }

    doc_v18 = {
        "semantic_flow": build_doc_semantic_flow_v18(safe_text),
        "tutorial": reconstruct_tutorial_v18(safe_text),
        "concept_graph": build_doc_concept_graph_v18(safe_text),
        "chunks": chunk_semantic_v18(safe_text),
        "api_contracts": extract_api_contracts_v18(safe_text),
        "architecture_docs": extract_architecture_sections_v18(safe_text),
        "dependency_references": extract_dependency_references_v18(safe_text),
        "migration": extract_migration_guides_v18(safe_text),
    }
    normalized["content"]["documents"]["reconstruction_v18"] = doc_v18

    canonical_sources_v18 = canonicalize_source_set([u for u in [source_url] + refs if u])
    internet_v18 = {
        "sources": canonical_sources_v18,
        "trust": score_trust(source_url),
        "freshness": score_freshness({"sources": len(canonical_sources_v18)}),
        "dedup_sources": resolve_duplicate_sources([{"url": u} for u in canonical_sources_v18]),
        "source_merge": merge_semantic_sources([{"source_url": source_url, "text_len": len(safe_text)}]),
        "crawl_priority": rank_crawl_priority(canonical_sources_v18),
        "repository_authority": score_repository_authority(source_url),
    }
    if len(canonical_sources_v18) >= 2:
        internet_v18["semantic_similarity"] = semantic_similarity(canonical_sources_v18[0], canonical_sources_v18[1])
    else:
        internet_v18["semantic_similarity"] = {"score": 1.0}
    normalized["content"]["internet"]["intelligence_v18"] = internet_v18

    universal_v18 = {
        "openapi": parse_openapi(safe_text),
        "graphql": parse_graphql(safe_text),
        "protobuf": parse_protobuf(safe_text),
        "notebook": parse_notebook(safe_text),
        "archive": inspect_archive_v4(source_url or safe_text[:256]),
        "cicd": parse_cicd_v4(safe_text),
        "infra": parse_infra_v4(safe_text),
        "binary_boundary": inspect_binary_boundary_v4(safe_text),
    }
    normalized["content"]["universal_v18"] = universal_v18

    graph_base_v18 = normalized.get("relationships", {}).get("execution_graph_v7", normalized.get("relationships", {}).get("execution_graph", {}))
    graph_bounded_v18 = graph_memory_bound_v18(graph_base_v18)
    graph_reasoned_v18 = {
        "reasoning": graph_reason_v18(graph_bounded_v18),
        "clusters": graph_cluster_v18(graph_bounded_v18),
        "partitions": graph_partition_v18(graph_bounded_v18),
        "search_document": graph_search_v18(graph_bounded_v18, "document"),
        "paths_document": semantic_paths(graph_bounded_v18, "document", depth=3),
        "traversal_document": graph_traverse_v18(graph_bounded_v18, "document"),
        "self_similarity": graph_similarity_v18(graph_bounded_v18, graph_bounded_v18),
        "self_diff": graph_diff_v18(graph_bounded_v18, graph_bounded_v18),
    }
    normalized["relationships"]["graph_reasoning_v18"] = graph_reasoned_v18
    normalized["relationships"]["execution_graph_v18"] = compress_graph_v18(graph_bounded_v18)

    knowledge_v18 = {
        "entities": resolve_entities_v18(symbols_v18.get("symbols", [])),
        "identity": build_semantic_identity(source_url or "input"),
        "concept_graph": build_concept_graph_v18(symbols_v18.get("symbols", [])),
        "repository_knowledge": build_repository_knowledge_v18(
            {
                "symbols": symbols_v18.get("symbols", []),
                "dependencies": parsed_v18.get("dependencies", {}).get("dependencies", []),
                "frameworks": normalized.get("content", {}).get("repository", {}).get("semantic_v17", {}).get("frameworks", []),
            }
        ),
        "documentation_knowledge": build_documentation_knowledge_v18(
            {
                "sections": [
                    str(s)
                    for s in doc_v18.get("semantic_flow", {}).get("nodes", [])
                ]
                if isinstance(doc_v18.get("semantic_flow", {}).get("nodes", []), list)
                else [],
                "references": doc_v18.get("api_contracts", {}).get("routes", []),
            }
        ),
        "architecture_knowledge": build_architecture_knowledge_v18(
            {
                "styles": arch_class_v18.get("styles", []),
                "relationships": event_v18.get("edges", []),
            }
        ),
        "dependency_knowledge": build_dependency_knowledge_v18(parsed_v18.get("dependencies", {}).get("dependencies", [])),
    }
    normalized["content"]["knowledge_reconstruction_v18"] = knowledge_v18

    normalized["metadata"]["quality_v18"] = {
        "ranked_extractions": [
            {
                "source_url": r.get("source_url", ""),
                "raw_text_len": len(r.get("raw_text", "") or ""),
                "edge_count": len(r.get("relationships", {}).get("execution_graph", {}).get("edges", [])),
            }
            for r in rank_extraction_results([normalized])
        ],
        "structure_score": score_structure_quality(graph_bounded_v18),
    }
    normalized["metadata"]["security_v18"] = {
        "ssrf": ssrf_guard(source_url) if source_url else {"ok": True},
        "redirect": redirect_guard([source_url] if source_url else []),
        "malformed_payload": malformed_payload_guard(safe_text),
        "recursion": recursion_guard(depth=0),
        "memory": memory_guard(len(safe_text.encode("utf-8", errors="ignore"))),
        "decompression": decompression_guard(1, len(safe_text.encode("utf-8", errors="ignore"))),
    }
    normalized["metadata"]["performance_v18"] = {
        "parser_pool": parser_pool(),
        "stream_chunks": len(stream_parse(safe_text)),
        "incremental_segments": len(incremental_parse(safe_text).get("segments", [])),
        "budgeted_chunks": len(budgeted_chunks(safe_text)),
        "memory_budget": memory_budget(len(safe_text.encode("utf-8", errors="ignore"))),
        "timeout": timeout_guard(0.0),
        "lazy_preview": lazy_extract(safe_text, ["length", "preview"]),
    }
    normalized["metadata"]["observability_v18"] = {
        "diagnostics": extraction_diagnostics(normalized),
        "metrics": performance_metrics({"extract_ms": 0.0}),
        "trace": deterministic_trace(source_url or "input"),
    }

    canonical = dumps_deterministic(normalized)
    normalized["metadata"]["serialization_v4"] = {"canonical_length": len(canonical)}
    normalized["metadata"]["serialization_v5"] = {"canonical_length": len(canonical)}
    normalized["fingerprint"] = fingerprint_v3(normalized)
    return normalized
