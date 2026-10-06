#!/usr/bin/env python3
"""Export bilingual essays from the Obsidian vault into the Jekyll `_essays/` collection.

The vault is the source of truth. Only the `## 🇺🇸 …` and `## 🇧🇷 …` sections of
each note are published; everything else in the note stays private.

Usage:
    uv run scripts/export_from_vault.py --out _essays <essay-folder> [<essay-folder> ...]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

SERIES: dict[str, str] = {"The Future of Software": "the-future-of-software"}

FLAG_EN = "🇺🇸"
FLAG_PT = "🇧🇷"
SOURCES = "🔗"
ESSAY_PREFIX = "✍️"
ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}
GENERATED_MARK = "generated: true"


class ExportError(ValueError):
    """Raised when a vault note cannot be exported safely."""


@dataclass(frozen=True)
class Essay:
    slug: str
    title_en: str
    title_pt: str
    body_en: str
    body_pt: str
    description: str
    description_pt: str
    date: str
    series: str
    part: int
    order: int
    sources: str = ""


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def slugify(title: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


def _frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ExportError("note has no YAML frontmatter")
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    return meta, text[match.end():]


def _sections(body: str) -> dict[str, tuple[str, str]]:
    """Map heading flag -> (title, content) for level-2 headings."""
    found: dict[str, tuple[str, str]] = {}
    parts = re.split(r"^## (.+)$", body, flags=re.MULTILINE)
    for heading, content in zip(parts[1::2], parts[2::2]):
        heading = heading.strip()
        for flag in (FLAG_EN, FLAG_PT, SOURCES):
            if heading.startswith(flag):
                found[flag] = (heading[len(flag):].strip(), content)
    return found


def _clean(content: str) -> str:
    content = re.sub(r"\[\[[^\]|]+\|([^\]]+)\]\]", r"\1", content)
    content = re.sub(r"\[\[([^\]]+)\]\]", r"\1", content)
    lines = [line for line in content.splitlines() if line.strip() != "---"]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def _sources(content: str) -> str:
    """Markdown bullet list of sources; every bullet must carry a link."""
    bullets = [line.strip() for line in _clean(content).splitlines() if line.strip()]
    for line in bullets:
        if not line.startswith("- ") or not re.search(r"\]\(https?://[^)\s]+\)", line):
            raise ExportError(f"source line needs a '- ' bullet with a markdown link: {line!r}")
    return "\n".join(bullets)


def _first_paragraph(body: str) -> str:
    return " ".join(body.split("\n\n", 1)[0].split())


def parse_essay(text: str) -> Essay:
    text = _nfc(text).replace("\r\n", "\n")
    meta, body = _frontmatter(text)

    series_name = meta.get("series", "")
    if series_name not in SERIES:
        raise ExportError(f"unknown series {series_name!r}; known: {sorted(SERIES)}")

    part_match = re.match(r"Parte\s+([IVX]+)\b", meta.get("part", ""))
    if not part_match or part_match.group(1) not in ROMAN:
        raise ExportError(f"cannot read part from {meta.get('part')!r}")

    try:
        order = int(meta["order"])
    except (KeyError, ValueError) as exc:
        raise ExportError(f"cannot read order from {meta.get('order')!r}") from exc

    date = meta.get("date added", "")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise ExportError(f"cannot read 'date added' from {date!r}")

    sections = _sections(body)
    for flag in (FLAG_EN, FLAG_PT):
        if flag not in sections:
            raise ExportError(f"missing '## {flag}' section")

    title_en, raw_en = sections[FLAG_EN]
    title_pt, raw_pt = sections[FLAG_PT]
    body_en, body_pt = _clean(raw_en), _clean(raw_pt)
    if not body_en or not body_pt:
        raise ExportError(f"empty language section in {title_en!r}")

    return Essay(
        slug=slugify(title_en),
        title_en=title_en,
        title_pt=title_pt,
        body_en=body_en,
        body_pt=body_pt,
        description=_first_paragraph(body_en),
        description_pt=_first_paragraph(body_pt),
        date=date,
        series=SERIES[series_name],
        part=ROMAN[part_match.group(1)],
        order=order,
        sources=_sources(sections[SOURCES][1]) if SOURCES in sections else "",
    )


def _q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_essay(e: Essay) -> str:
    return "\n".join(
        [
            "---",
            "layout: essay",
            GENERATED_MARK,
            f"permalink: {_q(f'/essays/{e.slug}/')}",
            f"title: {_q(e.title_en)}",
            f"title_en: {_q(e.title_en)}",
            f"title_pt: {_q(e.title_pt)}",
            f"description: {_q(e.description)}",
            f"description_pt: {_q(e.description_pt)}",
            f"date: {e.date}",
            f"series: {e.series}",
            f"part: {e.part}",
            f"order: {e.order}",
            "---",
            "",
            '<section lang="en" markdown="1">',
            "",
            e.body_en,
            "",
            "</section>",
            "",
            '<section lang="pt-BR" markdown="1">',
            "",
            e.body_pt,
            "",
            "</section>",
            "",
            *_render_sources(e.sources),
        ]
    )


def _render_sources(sources: str) -> list[str]:
    if not sources:
        return []
    return [
        '<aside class="sources" markdown="1">',
        "",
        '<p class="sources-label"><span lang="en">Based on</span><span lang="pt-BR">Baseado em</span></p>',
        "",
        sources,
        "",
        "</aside>",
        "",
    ]


def _is_generated(path: Path) -> bool:
    head = path.read_text(encoding="utf-8").split("\n---", 1)[0]
    return GENERATED_MARK in head.splitlines()


def export(folders: list[Path], out_dir: Path) -> list[Path]:
    essays: list[Essay] = []
    for folder in folders:
        if not folder.is_dir():
            raise ExportError(f"not a folder: {folder}")
        for path in sorted(folder.iterdir()):
            if path.suffix == ".md" and _nfc(path.name).startswith(ESSAY_PREFIX):
                try:
                    essays.append(parse_essay(path.read_text(encoding="utf-8")))
                except ExportError as exc:
                    raise ExportError(f"{path.name}: {exc}") from exc

    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.md"):
        if _is_generated(old):
            old.unlink()

    written = []
    for e in essays:
        target = out_dir / f"{e.order:02d}-{e.slug}.md"
        target.write_text(render_essay(e), encoding="utf-8", newline="\n")
        written.append(target)
    return sorted(written)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, required=True, help="Jekyll collection folder")
    parser.add_argument("folders", type=Path, nargs="+", help="vault essay folders")
    args = parser.parse_args(argv)
    try:
        written = export(args.folders, args.out)
    except ExportError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"{len(written)} essays exported")
    return 0


if __name__ == "__main__":
    sys.exit(main())
