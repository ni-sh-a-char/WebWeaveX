package io.webweavex

import io.webweavex.repository.*
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class IndexingTest {
    @Test
    fun `tokenizer splits whitespace`() {
        val tokens = DeterministicTokenizer.tokenize("hello world test")
        assertEquals(3, tokens.size)
        assertEquals("hello", tokens[0])
    }



    @Test
    fun `tokenizer is deterministic`() {
        val t1 = DeterministicTokenizer.tokenize("hello world")
        val t2 = DeterministicTokenizer.tokenize("hello world")
        assertEquals(t1, t2)
    }

    @Test
    fun `tokenizer handles empty input`() {
        assertEquals(emptyList(), DeterministicTokenizer.tokenize(""))
        assertEquals(emptyList(), DeterministicTokenizer.tokenizeCamelCase(""))
    }

    @Test
    fun `search index uses tokenization`() {
        val graph = KnowledgeGraph(
            listOf(
                KnowledgeNode("n1", "file", mapOf("name" to "hello world")),
                KnowledgeNode("n2", "module", mapOf("name" to "other"))
            ),
            emptyList()
        )
        val index = SearchIndex.build(graph)
        val results = index.search("hello")
        assertEquals(1, results.size)
        assertEquals("n1", results[0])
    }

    @Test
    fun `search index type search`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "file", mapOf("name" to "a")), KnowledgeNode("n2", "module", mapOf("name" to "b"))),
            emptyList()
        )
        val index = SearchIndex.build(graph)
        val results = index.searchByType("file")
        assertEquals(1, results.size)
        assertEquals("n1", results[0])
    }

    @Test
    fun `search index field search`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "file", mapOf("status" to "active"))),
            emptyList()
        )
        val index = SearchIndex.build(graph)
        val results = index.searchByField("status", "active")
        assertEquals(1, results.size)
    }

    @Test
    fun `search index is deterministic`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "file", mapOf("data" to "test"))),
            emptyList()
        )
        val i1 = SearchIndex.build(graph)
        val i2 = SearchIndex.build(graph)
        assertEquals(i1.fingerprint, i2.fingerprint)
    }

    @Test
    fun `search index handles empty graph`() {
        val index = SearchIndex.build(KnowledgeGraph(emptyList(), emptyList()))
        assertTrue(index.search("test").isEmpty())
    }
}
