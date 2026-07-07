package io.webweavex

import io.webweavex.determinism.StableSerialize
import java.lang.reflect.Method
import java.lang.reflect.Modifier
import java.security.MessageDigest
import kotlin.system.exitProcess

// Cross-language harness (Python -> Kotlin), mirroring
// tool/convergence/JavaVerify.java. Reflectively invokes each API's static
// method (name -> class from java_index.json — reused as-is: Kotlin ports
// live at the same io.webweavex.* FQCN as their verified Java counterparts,
// so Class.forName resolves to the Kotlin class on this module's classpath),
// canonicalizes with io.webweavex.determinism.StableSerialize, sha256,
// compares to the Python-generated vector hash. Reports MATCH/DIFFER/MISSING.
//
// Run: kotlinc + `kotlin -cp <classes> io.webweavex.KotlinVerifyKt <vectors.json> <java_index.json>`
// or via the Gradle `verify` task once wired.
//
// ponytail: no BehaviorAliasMap.json/InvocationAdapterMap.json lookups yet —
// every K0 vector's `camel` name already equals its Kotlin method name 1:1.
// Add alias/adapter handling (same as JavaVerify) in K1+ if a ported API's
// name or signature diverges from Java's.

private fun sha256Hex(s: String): String {
    val digest = MessageDigest.getInstance("SHA-256").digest(s.toByteArray(Charsets.UTF_8))
    val sb = StringBuilder(digest.size * 2)
    for (b in digest) sb.append(String.format("%02x", b))
    return sb.toString()
}

@Suppress("UNCHECKED_CAST")
fun main(args: Array<String>) {
    if (args.size < 2) {
        System.err.println("usage: KotlinVerify <vectors.json> <java_index.json>")
        exitProcess(2)
    }
    val doc = parseJsonFile(args[0]) as Map<String, Any?>
    val index = parseJsonFile(args[1]) as Map<String, Any?>
    val vectors = doc["vectors"] as List<Map<String, Any?>>

    var pass = 0
    var diff = 0
    var miss = 0

    for (v in vectors) {
        if (v["error"] != null) {
            println("  SKIP " + v["api"])
            continue
        }
        val api = v["api"] as String
        val camel = (v["camel_java"] as? String) ?: (v["camel"] as String)
        val argList: List<Any?> = (v["args"] as? List<Any?>) ?: listOf(v["input"])

        val cls = index[camel] as? String
        if (cls == null) {
            println("  MISSING-KT $api")
            miss++
            continue
        }
        try {
            val clazz = Class.forName(cls)
            val target: Method? = clazz.methods.firstOrNull {
                it.name == camel && Modifier.isStatic(it.modifiers) && it.parameterCount == argList.size
            }
            if (target == null) {
                println("  MISSING-KT $api")
                miss++
                continue
            }
            val out = target.invoke(null, *argList.toTypedArray())
            val h = sha256Hex(StableSerialize.stableSerialize(out))
            val expected = v["output_sha256"] as String
            if (h == expected) {
                println("  MATCH  $api")
                pass++
            } else {
                println("  DIFFER $api\n    py=${expected.take(24)}\n    kt=${h.take(24)}")
                diff++
            }
        } catch (t: Throwable) {
            // Covers ClassNotFoundException too: classes not yet ported in this
            // Kotlin module report here rather than as a hard MISSING, exactly
            // like JavaVerify's own Class.forName-inside-try structure.
            println("  ERROR  $api: ${t.javaClass.simpleName} ${t.message}")
            miss++
        }
    }

    println("\nKotlin vs Python: $pass match, $diff differ, $miss missing/error")
    if (diff > 0) exitProcess(1)
}
