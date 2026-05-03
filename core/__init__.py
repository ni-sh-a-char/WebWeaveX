"""
WebWeaveX Core (PRIVATE)

This module is for internal use only.
External packages should use 'webweavex.run()' instead.

Public API is available via:
    from webweavex import run
"""

__all__ = []

__version__ = "v1_phase_14"


def __getattr__(name):
    raise ImportError(
        f"'{name}' is not publicly accessible.\n"
        "Use 'from webweavex import run' for the public API."
    )