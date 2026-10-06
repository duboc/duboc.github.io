import sys
import unicodedata
from dataclasses import replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from export_from_vault import (  # noqa: E402
    ExportError,
    export,
    parse_essay,
    render_essay,
    slugify,
)

EN_HOOK = "Good code was always ergonomics for humans."

SAMPLE = f"""---
tags: [essays, writing]
date added: 2026-09-25
series: The Future of Software
part: Parte II — Ofício
order: 8
status: draft
---

# ✍️ 08 — Good Code for Whom

> Série: [[🗂️ Essays — The Future of Software (Hub)]] · Parte II — Ofício · EN 200 palavras · PT 210 palavras

---

## 🇺🇸 Good Code for Whom?

{EN_HOOK}

Readability served the reader, and the reader is changing. See [[Some Note|alias]].

---

## 🇧🇷 Código Bom Para Quem?

Código bom sempre foi ergonomia para humanos.

A legibilidade servia ao leitor, e o leitor está mudando.

---

## 🌱 Texto-Semente Original

> Seed quote that must never be published.
"""


def test_slugify():
    assert slugify("Good Code for Whom?") == "good-code-for-whom"
    assert slugify("Fire, Not Engine") == "fire-not-engine"
    assert slugify("Código Bom") == "codigo-bom"


def test_parse_sections_and_metadata():
    e = parse_essay(SAMPLE)
    assert (e.title_en, e.title_pt) == ("Good Code for Whom?", "Código Bom Para Quem?")
    assert (e.series, e.part, e.order, e.date) == ("the-future-of-software", 2, 8, "2026-09-25")
    assert e.slug == "good-code-for-whom"
    assert e.description == EN_HOOK
    assert e.description_pt == "Código bom sempre foi ergonomia para humanos."


def test_parse_drops_vault_only_content():
    e = parse_essay(SAMPLE)
    for body in (e.body_en, e.body_pt):
        assert "Série" not in body and "Texto-Semente" not in body
        assert "Seed quote" not in body
        assert "[[" not in body and "---" not in body
    assert "alias" in e.body_en and "Some Note" not in e.body_en


def test_parse_normalizes_nfc():
    e = parse_essay(unicodedata.normalize("NFD", SAMPLE))
    assert e.title_pt == unicodedata.normalize("NFC", "Código Bom Para Quem?")
    assert e.part == 2


def test_parse_missing_language_fails():
    with pytest.raises(ExportError, match="🇧🇷"):
        parse_essay(SAMPLE.split("## 🇧🇷")[0])


def test_parse_unknown_series_fails():
    with pytest.raises(ExportError, match="series"):
        parse_essay(SAMPLE.replace("The Future of Software", "Other"))


def test_render_escapes_yaml():
    out = render_essay(replace(parse_essay(SAMPLE), title_en='Say "hi": now?'))
    assert 'title_en: "Say \\"hi\\": now?"' in out
    assert 'permalink: "/essays/good-code-for-whom/"' in out
    assert "generated: true" in out
    assert '<section lang="en" markdown="1">' in out
    assert '<section lang="pt-BR" markdown="1">' in out


def _vault(tmp_path):
    src = tmp_path / "vault"
    src.mkdir()
    (src / "✍️ 08 — Good Code for Whom.md").write_text(SAMPLE, encoding="utf-8")
    (src / "🗂️ Essays — The Future of Software (Hub).md").write_text("# hub\n", encoding="utf-8")
    out = tmp_path / "_essays"
    out.mkdir()
    return src, out


def test_export_writes_and_is_idempotent(tmp_path):
    src, out = _vault(tmp_path)
    first = export([src], out)
    content = first[0].read_text(encoding="utf-8")
    second = export([src], out)
    assert [p.name for p in first] == ["08-good-code-for-whom.md"] == [p.name for p in second]
    assert second[0].read_text(encoding="utf-8") == content
    assert sorted(p.name for p in out.iterdir()) == ["08-good-code-for-whom.md"]


def test_export_removes_stale_generated_files(tmp_path):
    src, out = _vault(tmp_path)
    (out / "99-old.md").write_text("---\ngenerated: true\n---\n", encoding="utf-8")
    (out / "manual.md").write_text("---\ntitle: keep\n---\n", encoding="utf-8")
    export([src], out)
    assert not (out / "99-old.md").exists()
    assert (out / "manual.md").exists()


SOURCE_LINE = (
    "- Thorsten Ball, [*What I believe about the future of software development*]"
    "(https://thorstenball.com/blog/2026/09/19/what-i-believe-about-the-future-of-software-development/), "
    "September 2026."
)
WITH_SOURCES = SAMPLE.replace(
    "## 🌱 Texto-Semente Original",
    f"## 🔗 Fontes\n\n{SOURCE_LINE}\n\n---\n\n## 🌱 Texto-Semente Original",
)


def test_parse_drops_sources_section():
    e = parse_essay(WITH_SOURCES)
    out = render_essay(e)
    assert "Fontes" not in e.body_pt and "thorstenball" not in e.body_pt
    assert "thorstenball" not in out
    assert "Based on" not in out and "Baseado em" not in out
    assert 'class="sources"' not in out
