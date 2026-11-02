"""Global (tiny) configuration: default language of error messages."""

from __future__ import annotations

_SUPPORTED = ("fa", "en")
_default_language = "fa"


def set_default_language(lang: str) -> None:
    """Set the language used by ``ValidationResult.message`` ("fa" or "en")."""
    global _default_language
    if lang not in _SUPPORTED:
        raise ValueError(f"unsupported language {lang!r}; choose one of {_SUPPORTED}")
    _default_language = lang


def get_default_language() -> str:
    return _default_language
