# duboc.github.io — Personal Blog Design

**Date:** 2026-10-06 · **Status:** draft for review

## Goal

Turn `duboc.github.io` (today a 2020 "Hello World") into Anderson Duboc's
personal blog: a place to publish thinking in public. The first content is
the essay series **The Future of Software** (13 one-page essays, EN + PT),
plus the standalone essay **The Whiteboard Defense**. More essays and series
will follow.

## Success criteria

1. `https://duboc.github.io/` lists the series and standalone essays.
2. Every essay has one stable URL with an EN/PT toggle.
3. Republishing after an edit in the Obsidian vault is one command + push.
4. Zero build infrastructure beyond native GitHub Pages (no Actions).
5. Links shared on LinkedIn render a proper title/description preview.

## Decisions

| Area | Decision |
|---|---|
| Repo | `duboc/duboc.github.io`, branch `master`, Pages from `/` (already configured) |
| Local clone | `~/local/projects/duboc.github.io` |
| Engine | Native GitHub Pages Jekyll, no custom Actions |
| Theme | No remote theme. Own minimal layouts + one stylesheet |
| Plugins | `jekyll-feed` (RSS at `/feed.xml`), `jekyll-seo-tag` (OG/Twitter cards). Both Pages-whitelisted |
| Site title | **Anderson Duboc** |
| Tagline | EN: *Thinking out loud about software, AI, and the people who build it.* · PT: *Pensando em voz alta sobre software, IA e as pessoas que constroem.* |
| Footer | © Anderson Duboc · *Views are my own.* · GitHub · RSS |
| Source of truth | The Obsidian vault. The repo holds a generated export |
| Draft status | Vault `status: draft` essays are published as-is |

## Information architecture

| URL | Content |
|---|---|
| `/` | Home: tagline, series card(s), standalone essays, newest first |
| `/the-future-of-software/` | Series hub: one-line framing question, essays grouped by the 5 parts |
| `/essays/<slug>/` | One essay. Prev/next within its series |
| `/feed.xml` | RSS (jekyll-feed, collection `essays`) |

Slugs come from the English title: `fire-not-engine`, `post-binary`, …,
`the-whiteboard-defense`. Essay URLs do not include the series, so an essay
can join or leave a series without breaking links.

## Content model

Jekyll collection `_essays/`, `output: true`, permalink `/essays/:slug/`.

```yaml
---
title_en: "Fire, Not Engine"
title_pt: "Fogo, Não Motor"
title: "Fire, Not Engine"        # for seo-tag / feed
description: "There are decades where nothing happens, and weeks where decades happen."
description_pt: "Há décadas em que nada acontece e semanas em que décadas acontecem."
date: 2026-09-25
series: the-future-of-software  # omitted for standalone essays
part: 1                         # 1..5, series only
order: 1                        # series only
layout: essay
---
<section lang="en" markdown="1">
...English body...
</section>

<section lang="pt-BR" markdown="1">
...Portuguese body...
</section>
```

- `description` = first paragraph (the hook) of the EN text. The PT hook is
  stored as `description_pt` and used on listings when PT is active.
- Series metadata lives in `_data/series.yml`: slug, titles EN/PT, framing
  question EN/PT, and part names EN/PT
  (I Discovery/Descoberta, II Craft/Ofício, III People/Pessoas,
  IV Platform/Plataforma, V Closing/Fechamento).

## Language toggle

- Both languages ship in the same HTML.
- Without JS: both sections render stacked (EN first). Nothing is hidden.
- With JS (inline, < 40 lines): adds `js` + `data-lang` to `<html>`.
  Language priority: `?lang=pt|en` → `localStorage` → `navigator.language`
  (`pt*` → PT) → EN.
- CSS hides the inactive language only under `.js`. A header button
  `EN | PT` switches, persists to `localStorage`, and updates `<html lang>`.
- Titles and listing hooks use `<span lang="…">` pairs, toggled the same way.

## Visual design

Typographic, quiet, reading-first: system serif for body (~19–20px),
system sans for UI, measure ~65ch, generous line-height, light/dark through
`prefers-color-scheme`, a single accent color. No web fonts, no images, no
tracking, no external requests.

## Vault → repo export

`scripts/export_from_vault.py` (Python stdlib, run with `uv run`):

- Input: vault essays folder (`--vault` argument or `NOTAS_VAULT` env var;
  no personal path hardcoded in the repo). Reads every `✍️ *.md` under
  `30_ATLAS/essays/` recursively.
- Keeps **only** the `## 🇺🇸 …` and `## 🇧🇷 …` sections. Everything else
  (the vault header line, word counts, wikilinks, "how to incorporate"
  notes, original seed text) is dropped.
- Titles come from those two headings with the flag removed.
- Series/part/order come from the vault frontmatter (`series`, `part`,
  `order`). `series: Standalone…` → no series.
- Normalizes Unicode to NFC (macOS APFS filenames are NFD).
- Writes `_essays/<NN>-<slug>.md` (series) or `_essays/<slug>.md`
  (standalone). Deterministic: running it twice yields no diff.
- Fails loudly if an essay lacks either language section.

## Repository layout

```text
_config.yml          site config, collection, plugins, exclude list
_layouts/            default.html, essay.html, series.html
_includes/           head.html, header.html (toggle), footer.html
_data/series.yml
_essays/             generated by the export script
assets/style.css     (toggle JS is inlined in head.html to avoid a flash of both languages)
index.html           home
the-future-of-software.html   series hub (layout: series)
404.html
scripts/export_from_vault.py
tests/test_export.py
Justfile             quick (pytest) · export · check (live URL check)
AGENTS.md            repo rules for agents
README.md
docs/superpowers/    specs + plans (excluded from the site)
```

`_config.yml` excludes `docs/`, `scripts/`, `tests/`, `Justfile`,
`AGENTS.md`, `README.md`, `pyproject.toml`, `uv.lock`.

## Verification

- `just quick` → `uv run --with pytest pytest -q tests/` covering: section
  split, dropped extra sections, wikilink removal, slugging, frontmatter
  mapping, standalone handling, NFC normalization, idempotence, failure on
  missing language.
- No local Jekyll (system Ruby 2.6, no Docker). Site build is verified on
  GitHub: `gh api repos/duboc/duboc.github.io/pages/builds/latest` must be
  `built`, then `just check` curls `/`, the series hub, all 14 essay URLs,
  `/feed.xml`, and asserts HTTP 200 + both `lang="en"` and `lang="pt-BR"`
  present on essay pages.
- Manual: open the site in a browser, toggle EN/PT, check dark mode and mobile width.

## Vault side

- Add the site link to `🗂️ Essays — The Future of Software (Hub).md`.
- Append `## [2026-10-06] publish | duboc.github.io — The Future of Software` to `log.md`.

## Out of scope (YAGNI)

Comments, analytics, search, tags pages, custom domain, newsletter, images,
per-language URLs.
