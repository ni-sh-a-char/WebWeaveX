package io.webweavex.runtime

import io.webweavex.fingerprint.Fingerprint

data class RuntimeSnapshot(
    val nodes: List<Map<String, Any>>,
    val edges: List<Map<String, Any>>,
    val metadata: RuntimeMetadata,
    val fingerprint: String,
    val timestamp: Long = io.webweavex.runtime.DeterministicClock.now()
) {
    fun toMap(): Map<String, Any> = mapOf(
        "nodes" to nodes,
        "edges" to edges,
        "metadata" to metadata.toMap(),
        "fingerprint" to fingerprint,
        "timestamp" to timestamp
    )

    companion object {
        fun create(nodes: List<Map<String, Any>>, edges: List<Map<String, Any>>, metadata: RuntimeMetadata): RuntimeSnapshot {
            val fp = Fingerprint.compute(mapOf("nodes" to nodes, "edges" to edges, "metadata" to metadata.toMap()))
            return RuntimeSnapshot(nodes, edges, metadata, fp)
        }
    }
}
