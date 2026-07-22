package io.webweavex.fingerprint

import io.webweavex.determinism.StableSerialize
import java.security.MessageDigest

object Fingerprint {
    fun compute(value: Any?): String {
        val payload = StableSerialize.stableSerialize(value)
        val digest = MessageDigest.getInstance("SHA-256")
        val hash = digest.digest(payload.toByteArray(Charsets.UTF_8))
        return hash.joinToString("") { "%02x".format(it) }
    }

    fun computeGraph(nodes: List<Map<String, Any>>, edges: List<Map<String, Any>>): String {
        val sortedNodes = nodes.sortedBy { it["id"].toString() }
        val sortedEdges = edges.sortedBy { "${it["from"]}|${it["to"]}|${it["relation"]}" }
        return compute(mapOf("nodes" to sortedNodes, "edges" to sortedEdges))
    }

    /**
     * Kaalka-based graph fingerprint.
     * Matches Python graph_fingerprint: JSON sort_keys -> UTF-8 -> kaalka_encrypt(time_key=123456).
     */
    fun graphFingerprint(graph: Map<String, Any>): ByteArray {
        val payload = StableSerialize.stableSerialize(graph)
            .toByteArray(Charsets.UTF_8)
        return io.webweavex.crypto.KaalkaV5.encrypt(payload, "123456")
    }
}
