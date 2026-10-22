import logging
import re

from app.core.config import settings

# Safety net only: our code must never pass passwords or tokens to a logger.
# These patterns catch accidental leaks (ours or a library's) before output.
_REDACTIONS = [
    (re.compile(r"(?i)(bearer\s+)\S+"), r"\1***"),
    (re.compile(r"eyJ[\w-]+\.[\w-]+\.[\w-]+"), "***"),
    (re.compile(r"""(?i)(["']?(?:password|token|secret)["']?\s*[:=]\s*["']?)[^"'\s,}]+"""), r"\1***"),
]

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


def redact(text: str) -> str:
    for pattern, replacement in _REDACTIONS:
        text = pattern.sub(replacement, text)
    return text


class RedactingFormatter(logging.Formatter):
    """Formats a record (including any traceback), then strips secrets."""

    def format(self, record: logging.LogRecord) -> str:
        return redact(super().format(record))


def setup_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(LOG_FORMAT))

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(settings.log_level.upper())
