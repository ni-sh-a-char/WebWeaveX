package io.webweavex.replay

import io.webweavex.fingerprint.Fingerprint

/**
 * Replay equivalence validation — faithful Kotlin port of Python's
 * `validate_replay_equivalence` and Java's `ReplayEquivalence.validate`.
 *
 * Verifies a replayed extraction restored equivalent runtime graphs,
 * fingerprints, and browser identity. Output is deterministic and
 * cross-language compatible.
 */
object ReplayEquivalence {

    /**
     * Validate replay equivalence between original and replayed envelopes.
     *
     * Checks:
     * 1. Graph hash — normalized graph structure must match
     * 2. Global fingerprint — overall fingerprint must match
     * 3. Browser identity — runtime identity must match
     *
     * @param original Original extraction envelope
     * @param replayed Replayed extraction envelope
     * @return Map with "equivalent" (Boolean), "checks" (List), "bounded" (true)
     */
    fun validate(
        original: Map<String, Any>,
        replayed: Map<String, Any>
    ): Map<String, Any> {
        val origGraph = graphOf(original)
        val replayGraph = graphOf(replayed)

        val origFp = computeGlobalFingerprint(original, origGraph)
        val replayFp = computeGlobalFingerprint(replayed, replayGraph)

        val ghOrig = graphHash(origGraph)
        val ghReplay = graphHash(replayGraph)

        val checks = mutableListOf<Map<String, Any>>()
        checks.add(check("graph_hash", ghOrig == ghReplay, ghOrig.take(16), ghReplay.take(16)))
        checks.add(check("global_fingerprint", origFp == replayFp, origFp.take(16), replayFp.take(16)))

        val identityCheck = linkedMapOf<String, Any>(
            "name" to "browser_identity",
            "ok" to (identity(original) == identity(replayed))
        )
        checks.add(identityCheck)

        val equivalent = checks.all { (it["ok"] as? Boolean) == true }

        return linkedMapOf(
            "equivalent" to equivalent,
            "checks" to checks,
            "bounded" to true
        )
    }

    /**
     * Compute graph hash — normalized graph structure hash.
     * Matches Python _graph_hash and Java graphHash.
     */
    fun graphHash(graph: Map<String, Any>): String {
        val normalized = normalizeGraphContract(graph)
        val payload = linkedMapOf(
            "nodes" to (normalized["nodes"] ?: emptyList<Any>()),
            "edges" to (normalized["edges"] ?: emptyList<Any>())
        )
        return Fingerprint.compute(payload)
    }

    /**
     * Compute global runtime fingerprint for an envelope.
     * Simplified version matching Python's compute_global_runtime_fingerprint.
     */
    private fun computeGlobalFingerprint(
        envelope: Map<String, Any>,
        graph: Map<String, Any>
    ): String {
        val combined = linkedMapOf<String, Any>()
        combined["graph"] = graph
        combined["pipeline_hash"] = envelope["pipeline_hash"] ?: ""
        combined["bounded"] = envelope["bounded"] ?: true
        return Fingerprint.compute(combined)
    }

    /**
     * Extract graph from envelope — checks "unified_runtime_graph" then "graph".
     * Matches Python and Java graphOf().
     */
    private fun graphOf(envelope: Map<String, Any>): Map<String, Any> {
        val g = envelope["unified_runtime_graph"]
            ?: envelope["graph"]
            ?: emptyMap<String, Any>()
        @Suppress("UNCHECKED_CAST")
        return (g as? Map<String, Any>) ?: emptyMap()
    }

    /**
     * Extract browser identity from envelope.
     * Matches Python and Java identity().
     */
    private fun identity(envelope: Map<String, Any>): Any? {
        @Suppress("UNCHECKED_CAST")
        val browserIr = envelope["browser_ir"] as? Map<String, Any> ?: emptyMap<String, Any>()
        return browserIr["runtime_identity"]
    }

    /**
     * Normalize graph contract — sort nodes by ID, edges by source+target+type.
     * Matches Python RuntimeGraphContract.normalize and Java RuntimeGraph.normalizeContract.
     */
    private fun normalizeGraphContract(graph: Map<String, Any>): Map<String, Any> {
        @Suppress("UNCHECKED_CAST")
        val nodes = (graph["nodes"] as? List<Map<String, Any>>)?.sortedBy { it["id"].toString() } ?: emptyList()
        @Suppress("UNCHECKED_CAST")
        val edges = (graph["edges"] as? List<Map<String, Any>>)?.sortedBy {
            "${it["source"] ?: it["from"] ?: ""}|${it["target"] ?: it["to"] ?: ""}|${it["type"] ?: it["relation"] ?: ""}"
        } ?: emptyList()
        return linkedMapOf("nodes" to nodes, "edges" to edges)
    }

    private fun check(name: String, ok: Boolean, original: String, replay: String): Map<String, Any> {
        return linkedMapOf(
            "name" to name,
            "ok" to ok,
            "original" to original,
            "replay" to replay
        )
    }
}
