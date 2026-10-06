# AGENTS.md — duboc.github.io

Anderson Duboc's personal blog. Native GitHub Pages (Jekyll) from `master`, no Actions.

## Rules

- **Source of truth is the Obsidian vault**, not this repo. Never hand-edit `_essays/`;
  edit the vault note and re-export.
- Only the `## 🇺🇸` / `## 🇧🇷` sections of a vault essay may be published.
- Commits as `Anderson Duboc <andersonduboc@gmail.com>` (repo-local config). No AI trailers.
- No personal paths in the repo: the vault location comes from `NOTAS_VAULT`.
- No remote theme, web fonts, images, analytics or external requests.
  Plugins: `jekyll-feed`, `jekyll-seo-tag` only.

## Workflow

| Step | Command |
|---|---|
| Tests (run before every commit) | `just quick` |
| Re-export essays | `NOTAS_VAULT="…/notas" just export` |
| After push: Pages build status | `gh api repos/duboc/duboc.github.io/pages/builds/latest --jq .status` |
| After build: live check | `just check` |

## Gotchas

- No local Jekyll (system Ruby 2.6, no Docker): the site build is verified on GitHub.
- macOS filenames are NFD; the exporter normalizes to NFC.
- New series: add it to `SERIES` in `scripts/export_from_vault.py` and to `_data/series.yml`.
