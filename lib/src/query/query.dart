/// Family barrel for the WebWeaveX query / reasoning / IR public APIs.
///
/// Exports the camelCase public surface that mirrors the Python `__all__`
/// query/reasoning targets. Parity proven via `computeDeterministicHash`
/// (see test/parity/query_parity_test.dart and validation/parity/
/// query_api_vectors.json).
///
/// NOT exported as parity-proven (delegate to unported heavy IR compilers):
///   * compileDocument  — document_semantic_ir NLP pipeline
///   * compileRepository — repository_execution_ir AST/source parsing
/// They are still exported (throwing `UnsupportedError`) to keep the public
/// surface aligned with the Python `__all__`.
library;

export 'query_engines.dart'
    show
        queryGraph,
        queryRepo,
        queryRepository,
        queryDocuments,
        queryKnowledge,
        querySemantics,
        reasonSemantically,
        compileDocument,
        compileRepository,
        analyze;
