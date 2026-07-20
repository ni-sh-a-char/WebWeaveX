package io.webweavex.exceptions

open class WebWeaveXException(
    message: String,
    cause: Throwable? = null,
    val code: String = "WEBWEAVEX_ERROR"
) : Exception(message, cause)

class ValidationException(message: String) : WebWeaveXException(message, code = "VALIDATION_ERROR")
class ExtractionException(message: String) : WebWeaveXException(message, code = "EXTRACTION_ERROR")
class RepositoryException(message: String) : WebWeaveXException(message, code = "REPOSITORY_ERROR")
class ReplayException(message: String) : WebWeaveXException(message, code = "REPLAY_ERROR")
class FingerprintException(message: String) : WebWeaveXException(message, code = "FINGERPRINT_ERROR")
class SerializationException(message: String) : WebWeaveXException(message, code = "SERIALIZATION_ERROR")
class ConfigurationException(message: String) : WebWeaveXException(message, code = "CONFIGURATION_ERROR")
