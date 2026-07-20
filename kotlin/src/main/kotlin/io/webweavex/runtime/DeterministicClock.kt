package io.webweavex.runtime

/**
 * Deterministic clock abstraction.
 * Provides stable, reproducible timestamps for fingerprinting.
 * No runtime state that changes between executions.
 */
object DeterministicClock {
    private var offset = 0L

    fun now(): Long = 1000000000L + offset
    fun tick() { offset++ }
    fun reset() { offset = 0L }
    fun snapshot(): Long = now()
}
