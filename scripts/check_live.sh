#!/usr/bin/env bash
# Check the live site: home, series hub, feed, and every exported essay.
set -euo pipefail

BASE_URL="${BASE_URL:-https://duboc.github.io}"
cd "$(dirname "$0")/.."

failures=0
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

check() {
  local path="$1" bilingual="${2:-no}"
  local code
  code="$(curl -sS -L -o "$tmp" -w '%{http_code}' "${BASE_URL}${path}?cb=$(date +%s)" || echo 000)"
  if [[ "$code" != "200" ]]; then
    echo "FAIL $path HTTP $code"; failures=$((failures + 1)); return
  fi
  if [[ "$bilingual" == "yes" ]]; then
    if ! grep -q 'lang="en"' "$tmp" || ! grep -q 'lang="pt-BR"' "$tmp"; then
      echo "FAIL $path missing a language section"; failures=$((failures + 1)); return
    fi
  fi
  echo "OK   $path"
}

check "/"
if ! grep -q 'class="credit"' "$tmp"; then
  echo "FAIL / missing the inspiration credit"; failures=$((failures + 1))
fi
check "/the-future-of-software/"
if ! grep -q 'class="credit"' "$tmp"; then
  echo "FAIL /the-future-of-software/ missing the series credit"; failures=$((failures + 1))
fi
check "/feed.xml"

shopt -s nullglob
essays=(_essays/*.md)
if [[ ${#essays[@]} -eq 0 ]]; then
  echo "FAIL no essays in _essays/"; exit 1
fi

entries="$(curl -sS "${BASE_URL}/feed.xml?cb=$(date +%s)" | { grep -o '<entry>' || true; } | wc -l | tr -d ' ')"
if [[ "$entries" -lt ${#essays[@]} ]]; then
  echo "FAIL /feed.xml has $entries entries, expected ${#essays[@]}"; failures=$((failures + 1))
else
  echo "OK   /feed.xml entries=$entries"
fi
for file in "${essays[@]}"; do
  name="$(basename "$file" .md)"
  slug="${name#[0-9][0-9]-}"
  check "/essays/${slug}/" yes
done

if [[ $failures -gt 0 ]]; then
  echo "$failures check(s) failed"; exit 1
fi
echo "All checks passed"
