package io.webweavex

import io.webweavex.extract.*
import io.webweavex.fingerprint.Fingerprint
import io.webweavex.repository.*
import io.webweavex.memory.MemoryEngine
import io.webweavex.workflow.WorkflowEngine
import io.webweavex.workflow.WorkflowStep
import io.webweavex.replay.ReplayEngine
import io.webweavex.runtime.RuntimeKernel
import io.webweavex.runtime.RuntimeMetadata
import io.webweavex.serialization.CanonicalSerialization
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class EndToEndValidationTest {
    @Test
    fun `complete workflow: extraction to fingerprint`() {
        // Step 1: Extract
        val html = "<html><head><title>My Project</title></head>" +
                   "<body><h1>Architecture</h1><p>Layered design.</p>" +
                   "<a href=\"https://github.com/test\">Source</a></body></html>"
        val result = ExtractionPipeline.extractText(html)

        // Step 2: Verify extraction
        assertTrue(result.content.isNotEmpty())
        assertEquals("My Project", result.metadata["title"])

        // Step 3: Fingerprint
        val fp = result.fingerprint
        assertTrue(fp.isNotEmpty())
        assertEquals(64, fp.length)

        // Step 4: Determinism
        val result2 = ExtractionPipeline.extractText(html)
        assertEquals(result.fingerprint, result2.fingerprint)
    }

    @Test
    fun `complete workflow: repository analysis to knowledge graph`() {
        val text = "# My Project\n## Quick Start\npip install flask\nGET /api/users\nimport os"
        val summary = RepositoryAnalyzerEngine.analyze(java.io.File("."))

        // Step 1: Analyze repository
        assertTrue(summary.totalFiles >= 0)
        assertTrue(summary.fingerprint.isNotEmpty())

        // Step 2: Build knowledge graph
        val nodes = summary.readmeSections.mapIndexed { i, s ->
            KnowledgeNode("section_$i", "section", mapOf("title" to s))
        }
        val edges = nodes.windowed(2).map { KnowledgeEdge(it[0].id, it[1].id, "next") }
        val graph = KnowledgeGraph(nodes, edges)

        // Step 3: Query
        val queryResult = QueryEngine.search(graph, "Quick")
        assertTrue(queryResult.totalMatches >= 1)

        // Step 4: Fingerprint
        assertTrue(graph.fingerprint().isNotEmpty())
    }

    @Test
    fun `complete workflow: extraction pipeline with memory`() {
        // Create memory store
        var store = MemoryEngine.create()
        store = store.put("session_id", "test_001")

        // Extract content
        val html = "<html><body><h1>Test</h1><p>Content for analysis</p></body></html>"
        val extraction = ExtractionPipeline.extractText(html)

        // Store extraction result
        store = store.put("extraction_fingerprint", extraction.fingerprint)
        store = store.put("extraction_type", extraction.metadata["input_type"])

        // Verify memory
        assertEquals("test_001", store.get("session_id"))
        assertEquals(extraction.fingerprint, store.get("extraction_fingerprint"))
        assertTrue(store.fingerprint().isNotEmpty())
    }

    @Test
    fun `complete workflow: deterministic serialization pipeline`() {
        val data = mapOf(
            "repository" to mapOf("name" to "test", "language" to "Kotlin"),
            "extraction" to mapOf("html" to "<html>test</html>"),
            "metadata" to mapOf("version" to "3.0.0")
        )

        // Step 1: Serialize
        val serialized = CanonicalSerialization.serialize(data)
        assertTrue(serialized.contains("\"repository\""))
        assertTrue(serialized.contains("\"extraction\""))
        assertTrue(serialized.contains("\"metadata\""))

        // Step 2: Hash
        val hash1 = CanonicalSerialization.hash(data)
        val hash2 = CanonicalSerialization.hash(data)
        assertEquals(hash1, hash2)

        // Step 3: Deterministic ordering
        val sorted = CanonicalSerialization.serialize(mapOf("z" to 1, "a" to 2))
        assertEquals("""{"a":2,"z":1}""", sorted)
    }

    @Test
    fun `complete workflow: runtime kernel with extraction`() {
        val kernel = RuntimeKernel.create()
        val input = io.webweavex.runtime.UniversalInput(source = "<html>test</html>")
        val output = kernel.extract(input)

        assertTrue(output.isValid())
        assertEquals("3.0.0", output.version)
        assertTrue(output.fingerprint.isNotEmpty())
    }

    @Test
    fun `complete workflow: replay validation`() {
        // Create state
        val state = mapOf("extraction" to "data", "fingerprint" to "abc123")

        // Create snapshots
        val snap1 = io.webweavex.replay.ReplayEngine.createSnapshot(state, 0)
        val snap2 = io.webweavex.replay.ReplayEngine.createSnapshot(state, 1)

        // Validate equivalence
        assertTrue(io.webweavex.replay.ReplayEngine.validateEquivalence(snap1, snap2))

        // Replay
        val result = io.webweavex.replay.ReplayEngine.replay(listOf(snap1, snap2))
        assertTrue(result.equivalent)
        assertTrue(result.fingerprint.isNotEmpty())
    }

    @Test
    fun `complete workflow: memory persistence and query`() {
        var store = MemoryEngine.create()
        store = store.put("repo_name", "webweavex")
        store = store.put("repo_language", "Kotlin")
        store = store.put("repo_version", "3.0.0")
        store = store.put("extraction_count", 42)

        // Query memory
        assertEquals("webweavex", store.get("repo_name"))
        assertEquals(42, store.get("extraction_count"))
        assertEquals(4, store.size())
        assertTrue(store.keys().contains("repo_name"))
        assertTrue(store.fingerprint().isNotEmpty())

        // Snapshot
        val snapshot = store.snapshot()
        assertEquals(4, snapshot.entries.size)
        assertTrue(snapshot.fingerprint.isNotEmpty())
    }

    @Test
    fun `complete workflow: knowledge graph construction`() {
        // Build knowledge graph from extraction
        val extraction = ExtractionPipeline.extractText("<html><body><h1>API</h1></body></html>")
        val nodes = listOf(
            KnowledgeNode("doc_1", "document", mapOf("title" to "API", "fingerprint" to extraction.fingerprint)),
            KnowledgeNode("dep_1", "dependency", mapOf("name" to "kotlin-stdlib")),
            KnowledgeNode("dep_2", "dependency", mapOf("name" to "crypto"))
        )
        val edges = listOf(
            KnowledgeEdge("doc_1", "dep_1", "depends_on"),
            KnowledgeEdge("doc_1", "dep_2", "uses")
        )
        val graph = KnowledgeGraph(nodes, edges)

        // Verify
        assertEquals(3, graph.nodes.size)
        assertEquals(2, graph.edges.size)
        assertTrue(graph.fingerprint().isNotEmpty())

        // Query
        val results = QueryEngine.search(graph, "kotlin")
        assertTrue(results.totalMatches >= 1)
    }

    @Test
    fun `complete workflow: full pipeline`() {
        // 1. Extract HTML
        val extraction = ExtractionPipeline.extractText("<html><body><h1>Project</h1></body></html>")
        assertTrue(extraction.fingerprint.isNotEmpty())

        // 2. Serialize deterministically
        val serialized = CanonicalSerialization.serialize(extraction.toMap())
        assertTrue(serialized.isNotEmpty())

        // 3. Build knowledge graph
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "document", mapOf("fingerprint" to extraction.fingerprint))),
            listOf(KnowledgeEdge("n1", "n1", "self_reference"))
        )
        assertTrue(graph.fingerprint().isNotEmpty())

        // 4. Store in memory
        var store = MemoryEngine.create()
        store = store.put("extraction", extraction.toMap())
        store = store.put("graph_fingerprint", graph.fingerprint())
        assertTrue(store.fingerprint().isNotEmpty())

        // 5. Create workflow
        val steps = listOf(
            WorkflowStep("extract", { ExtractionPipeline.extractText(it["html"] as? String ?: "").toMap() }),
            WorkflowStep("serialize", { CanonicalSerialization.serialize(it).let { s -> mapOf("serialized" to s) } })
        )
        val workflowResult = WorkflowEngine.execute(steps, mapOf("html" to "<html>test</html>"))
        assertTrue(workflowResult.success)

        // 6. Replay
        val snap = io.webweavex.replay.ReplayEngine.createSnapshot(workflowResult.output, 0)
        val replayResult = io.webweavex.replay.ReplayEngine.replay(listOf(snap))
        assertTrue(replayResult.equivalent)
    }
}
