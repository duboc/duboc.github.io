# duboc.github.io

Thinking out loud about software, AI, and the people who build it.

Live at **https://duboc.github.io/**. First series: *The Future of Software* —
13 one-page essays, each in English and Portuguese.

## How it works

- Essays are written in an Obsidian vault and exported with
  `scripts/export_from_vault.py` into the Jekyll collection `_essays/`.
- GitHub Pages builds the site natively from `master`.

```bash
just quick                          # exporter tests
NOTAS_VAULT="/path/to/vault" just export
git push                            # Pages builds the site
just check                          # verify the live URLs
```

Views are my own.
