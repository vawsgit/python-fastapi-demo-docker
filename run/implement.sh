#!/bin/bash
# Implementation run for issue 12. A person approved run/plan.md and saved it as run/prompt.md.
# The run trusts five named tools. It never pushes, opens or merges a merge request; the script does that after it.
set -euo pipefail

git switch -c 12-filter-books-by-author

kiro-cli chat --v3 --no-interactive \
  --trust-tools=read,grep,glob,write,shell \
  "$(cat run/prompt.md)"

make check
