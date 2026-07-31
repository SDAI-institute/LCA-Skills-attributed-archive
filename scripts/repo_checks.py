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
    raw = raw.strip()
    if raw.startswith("<"):
        end = raw.find(">")
        return raw[1:end] if end >= 0 else raw[1:]

    # Markdown permits an optional quoted title after whitespace. Local paths in
    # this repository use percent-encoding rather than literal spaces.
    return raw.split(maxsplit=1)[0]


def _local_target(raw: str) -> str | None:
    target = _strip_optional_title(raw).strip()
    if not target or target.startswith("#"):
        return None
    target = target.replace("\\ ", " ")
    parsed = urlsplit(target)
    if parsed.scheme or target.startswith("//") or WINDOWS_ABSOLUTE_RE.match(target):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    return path


def _iter_targets(text: str) -> list[tuple[int, str]]:
    targets: list[tuple[int, str]] = []
    fence: str | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        marker = FENCE_RE.match(line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token[0]
            elif token[0] == fence:
                fence = None
            continue
        if fence is not None:
            continue
        definition = REFERENCE_DEF_RE.match(line)
        if definition:
            targets.append((line_number, definition.group("target")))
        for match in INLINE_LINK_RE.finditer(line):
            targets.append((line_number, match.group("target")))
    return targets


def find_broken_markdown_links(root: Path) -> tuple[int, list[BrokenMarkdownLink]]:
    """Check local Markdown links below ``root`` and return checked count/errors."""

    root = root.resolve()
    checked = 0
    broken: list[BrokenMarkdownLink] = []
    for source in sorted(root.rglob("*.md")):
        if excluded(source, root):
            continue
        text = source.read_text(encoding="utf-8")
        for line_number, raw in _iter_targets(text):
            target = _local_target(raw)
            if target is None:
                continue
            checked += 1
            if target.startswith("/"):
                resolved = (root / target.lstrip("/")).resolve()
            else:
                resolved = (source.parent / target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                broken.append(BrokenMarkdownLink(source, line_number, raw, resolved))
                continue
            if not resolved.exists():
                broken.append(BrokenMarkdownLink(source, line_number, raw, resolved))
    return checked, broken
