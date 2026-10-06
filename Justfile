set shell := ["bash", "-euo", "pipefail", "-c"]

# List recipes
default:
    @just --list

# Fast tests for the vault exporter
quick:
    uv run --with pytest pytest -q tests/

# Regenerate _essays/ from the Obsidian vault (requires NOTAS_VAULT)
export:
    @test -n "${NOTAS_VAULT:-}" || { echo "NOTAS_VAULT is not set" >&2; exit 1; }
    uv run scripts/export_from_vault.py --out _essays "$NOTAS_VAULT/30_ATLAS/essays/the-future-of-software"

# Check the live site (after the Pages build finishes)
check:
    bash scripts/check_live.sh
