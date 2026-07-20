package io.webweavex.memory

import io.webweavex.fingerprint.Fingerprint

data class MemoryEntry(val key: String, val value: Any?, val timestamp: Long = io.webweavex.runtime.DeterministicClock.now(), val fingerprint: String = "")

data class MemoryStore(val entries: Map<String, MemoryEntry> = emptyMap()) {
    fun put(key: String, value: Any?): MemoryStore {
        val entry = MemoryEntry(key, value, io.webweavex.runtime.DeterministicClock.now(), Fingerprint.compute(value))
        return copy(entries = entries + (key to entry))
    }

    fun get(key: String): Any? = entries[key]?.value
    fun has(key: String): Boolean = entries.containsKey(key)
    fun keys(): Set<String> = entries.keys.toSortedSet()
    fun size(): Int = entries.size
    fun fingerprint(): String = Fingerprint.compute(entries.keys.sorted().map { entries[it]?.value })
    fun snapshot(): MemorySnapshot = MemorySnapshot(entries, fingerprint())
}

data class MemorySnapshot(val entries: Map<String, MemoryEntry>, val fingerprint: String, val timestamp: Long = io.webweavex.runtime.DeterministicClock.now())

object MemoryEngine {
    fun create(): MemoryStore = MemoryStore()
    fun merge(a: MemoryStore, b: MemoryStore): MemoryStore = a.copy(entries = a.entries + b.entries)
}
