"""WebWeaveX public API."""

from core.crypto.kaalka_engine import hex_fingerprint as fingerprint
from core.crypto.kaalka_runtime_engine import encrypt_value, decrypt_value
from core.crypto.kaalka_session_engine import (
    encrypt_session_state,
    decrypt_session_state,
)
from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.session.encrypted_session_store import (
    save_encrypted_session,
    load_encrypted_session,
)
from core.auth import authenticate_runtime
from core.extract.pipeline import extract, extract_async, extract_docs, extract_repo
from core.intelligence.graph_analyzer import analyze_graph
from core.crawling.crawler_engine import crawl as _crawl
from core.streaming.streaming_pipeline import stream_extract
from core.agents.graph_query_engine import query_nodes, query_edges
from core.query.document_query_engine import query_documents as query_document_ir
from core.query.repository_query_engine import query_repository as query_repository_ir
from core.query.graph_query_engine import query_graph as query_graph_ir
from core.query.ontology_query_engine import query_knowledge as query_knowledge_ir
from core.query.semantic_query_engine import query_semantics
from core.ir.document_ir import compile_document_ir
from core.ir.repository_ir import compile_repository_ir
from core.reasoning.semantic_reasoning_engine import reason_semantically
from core.ingestion.universal_ingestion_engine import ingest_input
from webweavex.universal_extract import universal_extract
from core.browser.universal_web_extraction_engine import extract_web
from core.repository.universal_repository_extraction_engine import (
    extract_repository,
)
from core.multimodal.universal_multimodal_extraction_engine import (
    extract_multimodal,
)
from core.documents.universal_document_extraction_engine import (
    extract_document_runtime,
)
from core.runtime_graph import (
    build_runtime_graph,
    query_runtime_graph,
)
from core.interaction import (
    replay_interactions,
    extract_infinite_scroll,
    extract_paginated_content,
    build_interaction_graph,
)
from core.streaming import (
    capture_websocket_frames,
    capture_dom_mutations,
    replay_stream_events,
    build_stream_timeline,
)
from core.identity import (
    build_browser_identity,
    save_browser_identity,
    load_browser_identity,
)
from core.adaptive import (
    heal_selector,
    recover_modal_runtime,
    save_adaptive_memory,
    load_adaptive_memory,
)
from core.distributed_extraction import (
    run_autonomous_extraction,
    save_distributed_checkpoint,
    load_distributed_checkpoint,
)
from core.application import (
    run_application_cognition,
    execute_runtime_objective,
    save_application_memory,
    load_application_memory,
)
from core.native import (
    extract_native,
    run_native_cognition,
    save_native_runtime,
    load_native_runtime,
)
from core.causality import (
    run_causality_runtime,
    run_causality_for_extraction,
    save_causal_memory,
    load_causal_memory,
    replay_causal_runtime,
)
from core.semantic import (
    run_semantic_runtime,
    run_semantic_for_extraction,
    save_semantic_memory,
    load_semantic_memory,
    replay_semantic_runtime,
)
from core.workflows import (
    run_autonomous_workflow,
    run_workflow_for_extraction,
    build_runtime_objective,
    build_workflow_plan,
    save_workflow_memory,
    load_workflow_memory,
    replay_workflow_runtime,
)
from core.synchronization import (
    run_synchronized_runtime,
    run_sync_for_extraction,
    build_runtime_delta,
    save_sync_memory,
    load_sync_memory,
    replay_synchronized_runtime,
)
from core.evolution_runtime import (
    run_evolution_runtime,
    run_evolution_for_extraction,
    build_runtime_evolution,
    evolve_selector_runtime,
    save_evolution_runtime,
    load_evolution_runtime,
)
from core.connectors import (
    extract_database_runtime,
    extract_api_runtime,
    extract_runtime_streams,
    extract_container_runtime,
    extract_kubernetes_runtime,
    extract_telemetry_runtime,
    extract_ide_runtime,
    run_live_runtime,
    save_live_runtime,
    load_live_runtime,
)
from core.memory import (
    run_runtime_memory,
    run_memory_for_extraction,
    build_runtime_memory,
    save_runtime_memory,
    load_runtime_memory,
    search_runtime_memory,
    query_runtime_memory,
)
from core.execution import (
    run_execution_runtime,
    run_execution_for_extraction,
    execute_runtime_action,
    build_runtime_sandbox,
    simulate_runtime_execution,
    replay_runtime_execution,
)
from core.reconstruction import (
    run_reconstruction_runtime,
    run_reconstruction_for_extraction,
    reconstruct_runtime,
    fabricate_runtime_reality,
    clone_runtime_environment,
    validate_reconstructed_runtime,
)
from core.kernel import RuntimeKernel, get_runtime_kernel, run_canonical_pipeline
from core.contracts.runtime_contracts import UniversalInput
from core.determinism import compute_global_runtime_fingerprint
from core.replay import validate_replay_equivalence
from core.ir.unified_runtime_ir import compile_unified_runtime_ir
import asyncio

__version__ = "3.0.0"
version = __version__  # PEP 440 public version alias


def analyze(input_data, edges=None):
    """Analyze a graph or extract and analyze content.

    Args:
        input_data: Input data — either a dict with 'source' for extraction,
                    or nodes list for graph analysis.
        edges: Optional edges list for direct graph analysis.

    Returns:
        dict: Graph analysis with node_count, edge_count, density, degree_map.

    Example::

        result = wwx.analyze({"source": "<html>...</html>"})
        print(result["node_count"])
    """
    if edges is not None:
        return analyze_graph(input_data, edges)
    result = extract(input_data)
    graph = result.get("relationships", {}).get("execution_graph", {})
    return analyze_graph(graph.get("nodes", []), graph.get("edges", []))


def crawl(url: str, **kwargs):
    """Crawl a website and discover pages.

    Args:
        url: Starting URL to crawl.
        **kwargs: Additional crawler configuration.

    Returns:
        dict: Crawl results with visited URLs and discovered links.
    """
    return _crawl(url, **kwargs)


async def crawl_async(url: str, **kwargs):
    """Async version of crawl().

    Args:
        url: Starting URL to crawl.
        **kwargs: Additional crawler configuration.

    Returns:
        dict: Crawl results with visited URLs and discovered links.
    """
    return await asyncio.to_thread(_crawl, url, **kwargs)


def extract_recursive(url: str, **kwargs):
    """Recursively extract content from a URL — crawl + extract.

    Combines crawling and extraction into a single workflow.

    Args:
        url: URL to crawl and extract from.
        **kwargs: Additional configuration.

    Returns:
        dict: Extraction results with crawl metadata.
    """
    crawled = _crawl(url, **kwargs)
    out = extract(url)
    out["metadata"]["crawl"] = {"visited": crawled.get("visited", []), "discovered": crawled.get("discovered", [])}
    out["repository"] = out.get("content", {}).get("repository", {})
    out["documents"] = out.get("content", {}).get("documents", {})
    return out


def query_graph(result: dict = None, node: str = "", graph: dict = None):
    """Query a graph for nodes, edges, or traversal paths.

    Args:
        result: Extraction result containing a graph (optional).
        node: Starting node for traversal (optional).
        graph: Direct graph dict with nodes/edges (optional).

    Returns:
        dict: Graph query results.
    """
    if graph is not None:
        return query_graph_ir(graph, node=node)
    if result is None:
        return query_graph_ir({}, node=node)
    if "relationships" in result:
        g = result.get("relationships", {}).get("execution_graph", {})
    else:
        g = result
    return query_graph_ir(g, node=node)


def query_repo(result: dict):
    """Extract repository information from an extraction result.

    Args:
        result: Extraction result dict.

    Returns:
        dict: Repository data.
    """
    return result.get("content", {}).get("repository", {})


def query_knowledge(result: dict = None, entities=None, edges=None):
    """Query knowledge graph from extraction results or build one.

    Args:
        result: Extraction result (optional).
        entities: Entity list for direct query (optional).
        edges: Edge list for direct query (optional).

    Returns:
        dict: Knowledge graph data.
    """
    if entities is not None or edges is not None:
        return query_knowledge_ir(entities or [], edges or [])
    content = result.get("content", {}) if isinstance(result, dict) else {}
    return {
        "knowledge_v2": content.get("knowledge_v2", {}),
        "knowledge_v18": content.get("knowledge_reconstruction_v18", {}),
    }


def query_repository(result: dict = None, source: str = "", path: str = "", **kwargs):
    """Query repository intelligence.

    Args:
        result: Extraction result (optional).
        source: Repository source URL (optional).
        path: Repository path (optional).

    Returns:
        dict: Repository intelligence data.
    """
    if result is not None and not source:
        return query_repo(result)
    return query_repository_ir(source, path, kwargs.get("files"))


def query_documents(result: dict = None, text: str = ""):
    """Query document intelligence.

    Args:
        result: Extraction result (optional).
        text: Raw text to analyze (optional).

    Returns:
        dict: Document intelligence data.
    """
    if text:
        return query_document_ir(text)
    if result is not None:
        return result.get("content", {}).get("documents", {})
    return query_document_ir("")


def compile_document(text: str):
    """Compile a document into an intermediate representation.

    Args:
        text: Document text to compile.

    Returns:
        dict: Compiled document IR.
    """
    return compile_document_ir(text)


def compile_repository(source: str, path: str = "", **kwargs):
    """Compile a repository into an intermediate representation.

    Args:
        source: Repository source string or URL.
        path: Repository path (optional).

    Returns:
        dict: Compiled repository IR.
    """
    return compile_repository_ir(source, path, kwargs.get("files"))


__all__ = [
    "extract",
    "extract_async",
    "extract_repo",
    "extract_docs",
    "extract_recursive",
    "crawl",
    "crawl_async",
    "stream_extract",
    "query_graph",
    "query_repo",
    "query_repository",
    "query_documents",
    "query_knowledge",
    "query_semantics",
    "compile_document",
    "compile_repository",
    "reason_semantically",
    "fingerprint",
    "encrypt_value",
    "decrypt_value",
    "encrypt_session_state",
    "decrypt_session_state",
    "compute_kaalka_hash",
    "save_encrypted_session",
    "load_encrypted_session",
    "authenticate_runtime",
    "analyze",
    "ingest_input",
    "universal_extract",
    "extract_web",
    "extract_repository",
    "extract_multimodal",
    "extract_document_runtime",
    "build_runtime_graph",
    "query_runtime_graph",
    "replay_interactions",
    "extract_infinite_scroll",
    "extract_paginated_content",
    "build_interaction_graph",
    "capture_websocket_frames",
    "capture_dom_mutations",
    "replay_stream_events",
    "build_stream_timeline",
    "build_browser_identity",
    "save_browser_identity",
    "load_browser_identity",
    "heal_selector",
    "recover_modal_runtime",
    "save_adaptive_memory",
    "load_adaptive_memory",
    "run_autonomous_extraction",
    "save_distributed_checkpoint",
    "load_distributed_checkpoint",
    "run_application_cognition",
    "execute_runtime_objective",
    "save_application_memory",
    "load_application_memory",
    "extract_native",
    "run_native_cognition",
    "save_native_runtime",
    "load_native_runtime",
    "run_causality_runtime",
    "run_causality_for_extraction",
    "save_causal_memory",
    "load_causal_memory",
    "replay_causal_runtime",
    "run_semantic_runtime",
    "run_semantic_for_extraction",
    "save_semantic_memory",
    "load_semantic_memory",
    "replay_semantic_runtime",
    "run_autonomous_workflow",
    "run_workflow_for_extraction",
    "build_runtime_objective",
    "build_workflow_plan",
    "save_workflow_memory",
    "load_workflow_memory",
    "replay_workflow_runtime",
    "run_synchronized_runtime",
    "run_sync_for_extraction",
    "build_runtime_delta",
    "save_sync_memory",
    "load_sync_memory",
    "replay_synchronized_runtime",
    "run_evolution_runtime",
    "run_evolution_for_extraction",
    "build_runtime_evolution",
    "evolve_selector_runtime",
    "save_evolution_runtime",
    "load_evolution_runtime",
    "extract_database_runtime",
    "extract_api_runtime",
    "extract_runtime_streams",
    "extract_container_runtime",
    "extract_kubernetes_runtime",
    "extract_telemetry_runtime",
    "extract_ide_runtime",
    "run_live_runtime",
    "save_live_runtime",
    "load_live_runtime",
    "run_runtime_memory",
    "run_memory_for_extraction",
    "build_runtime_memory",
    "save_runtime_memory",
    "load_runtime_memory",
    "search_runtime_memory",
    "query_runtime_memory",
    "run_execution_runtime",
    "run_execution_for_extraction",
    "execute_runtime_action",
    "build_runtime_sandbox",
    "simulate_runtime_execution",
    "replay_runtime_execution",
    "run_reconstruction_runtime",
    "run_reconstruction_for_extraction",
    "reconstruct_runtime",
    "fabricate_runtime_reality",
    "clone_runtime_environment",
    "validate_reconstructed_runtime",
    "RuntimeKernel",
    "get_runtime_kernel",
    "run_canonical_pipeline",
    "UniversalInput",
    "compute_global_runtime_fingerprint",
    "validate_replay_equivalence",
    "compile_unified_runtime_ir",
    "__version__",
    "version",
]
