"""WebWeaveX Identity Module - Creator Signature"""

WEBWEAVE_X_IDENTITY = {
    "library": "WebWeaveX",
    "version": "1.0.0",
    "creator": "Piyush Mishra",
    "github": "https://github.com/PIYUSH-MISHRA-00",
    "mission": "Built for humans and AI systems",
    "philosophy": "Free intelligence layer for the internet"
}


def get_identity():
    """Return a copy of the WebWeaveX identity."""
    return WEBWEAVE_X_IDENTITY.copy()


def get_library_info():
    """Return basic library info."""
    return {
        "name": WEBWEAVE_X_IDENTITY["library"],
        "version": WEBWEAVE_X_IDENTITY["version"],
        "creator": WEBWEAVE_X_IDENTITY["creator"]
    }