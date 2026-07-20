package io.webweavex.replay

import io.webweavex.fingerprint.Fingerprint

data class ReplaySnapshot(
    val state: Map<String, Any>,
    val fingerprint: String,
    val stepIndex: Int,
    val timestamp: Long = io.webweavex.runtime.DeterministicClock.now()
)

data class ReplayResult(
    val snapshots: List<ReplaySnapshot>,
    val equivalent: Boolean,
    val fingerprint: String
)

object ReplayEngine {
    fun createSnapshot(state: Map<String, Any>, stepIndex: Int): ReplaySnapshot {
        val fp = Fingerprint.compute(state)
        return ReplaySnapshot(state, fp, stepIndex)
    }

    fun validateEquivalence(a: ReplaySnapshot, b: ReplaySnapshot): Boolean {
        return a.fingerprint == b.fingerprint
    }

    fun replay(snapshots: List<ReplaySnapshot>): ReplayResult {
        val last = snapshots.lastOrNull()
        val fp = last?.fingerprint ?: ""
        val allMatch = snapshots.all { it.fingerprint == fp }
        return ReplayResult(snapshots, allMatch, fp)
    }
}
