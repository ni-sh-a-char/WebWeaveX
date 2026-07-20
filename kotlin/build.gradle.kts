plugins {
    kotlin("jvm") version "1.9.22"
    `java-library`
    `maven-publish`
}

group = "io.webweavex"
version = "3.0.0" // synchronized with python/javascript/java/dart

repositories { mavenCentral() }

dependencies {
    testImplementation(kotlin("test-junit5"))
}

kotlin { jvmToolchain(17) }

tasks.test { useJUnitPlatform() }

publishing {
    publications { create<MavenPublication>("maven") { from(components["java"]) } }
}

