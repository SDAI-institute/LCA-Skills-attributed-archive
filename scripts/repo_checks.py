"""Reusable repository-level integrity checks."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

EXCLUDED_PARTS = {".git", ".venv", "__pycache__", "dist", "build", "release"}
INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\((?P<target><[^>]+>|[^)]+)\)")
REFERENCE_DEF_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(?P<target><[^>]+>|\S+)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")


@dataclass(frozen=True)
class BrokenMarkdownLink:
    """One unresolved local Markdown link."""

    source: Path
    line: int
    target: str
    resolved: Path

    def render(self, root: Path) -> str:
        try:
            source = self.source.relative_to(root)
        except ValueError:
            source = self.source
        try:
            resolved = self.resolved.relative_to(root)
        except ValueError:
            resolved = self.resolved
        return f"{source}:{self.line}: {self.target!r} -> {resolved}"


def excluded(path: Path, root: Path) -> bool:
    """Return whether a path belongs to generated or transient output."""

    try:
        parts = path.relative_to(root).parts
    except ValueError:
        parts = path.parts
    return bool(EXCLUDED_PARTS.intersection(parts))


def _strip_optional_title(raw: str) -> str:
