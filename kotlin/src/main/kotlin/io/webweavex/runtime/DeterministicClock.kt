package io.webweavex.runtime

/**
 * Thread-safe deterministic clock.
 * Uses an injected clock abstraction with no mutable global state.
 * Supports Runtime, Replay, and Test configurations.
 */
interface ClockProvider {
    fun now(): Long
}

class LogicalClock(private val baseTime: Long = 1000000000L, private val increment: Long = 0) : ClockProvider {
    override fun now(): Long = baseTime + increment
}

class ReplayClock(private val snapshots: List<Long>) : ClockProvider {
    private var index = 0
    override fun now(): Long = if (index < snapshots.size) snapshots[index++] else snapshots.lastOrNull() ?: 0L
}

class TestClock(private var time: Long = 1000000000L) : ClockProvider {
    override fun now(): Long = time
    fun advance(delta: Long) { time += delta }
    fun set(value: Long) { time = value }
}

object DeterministicClock {
    private val provider = java.util.concurrent.atomic.AtomicReference<ClockProvider>(LogicalClock())

    fun now(): Long = provider.get().now()
    fun setProvider(p: ClockProvider) { provider.set(p) }
    fun reset() { provider.set(LogicalClock()) }
}
