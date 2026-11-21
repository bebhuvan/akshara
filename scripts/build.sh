#!/usr/bin/env bash
# Build the site into public/: Hugo, then the search index. Needs hugo (version in .hugo-version) and npm ci.
set -euo pipefail
cd "$(dirname "$0")/.."
want="$(cat .hugo-version)"
have="$(hugo version | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | head -1 | tr -d v)"
if [ "$have" != "$want" ]; then
  echo "Hugo $want is needed; this machine has $have." >&2
  exit 1
fi
hugo --gc --minify --cleanDestinationDir --panicOnWarning
npx --no-install pagefind --site public --output-path public/pagefind
