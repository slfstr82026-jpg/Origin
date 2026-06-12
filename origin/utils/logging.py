"""Logging configuration helpers."""

from __future__ import annotations

import logging


def get_logger(name: str = "origin") -> logging.Logger:
    """Return a package logger with a default null handler."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(logging.NullHandler())
    return logger
