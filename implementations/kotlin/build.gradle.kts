plugins {
    kotlin("jvm") version "1.9.22"
    application
}

group = "com.webweavex"
version = "1.0.0"

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.jsoup:jsoup:1.17.2")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2")
    implementation("com.google.code.gson:gson:2.10.1")
}

kotlin {
    jvmToolchain(11)
}

application {
    mainClass.set("com.webweavex.ValidateKt")
}
