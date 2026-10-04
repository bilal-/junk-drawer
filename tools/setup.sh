#!/bin/sh
# One-time setup for a checkout: run tools/check.sh before every commit.
set -eu
unset CDPATH
cd "$(dirname "$0")/.."
mkdir -p .githooks
printf '#!/bin/sh\nexec tools/check.sh\n' > .githooks/pre-commit
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
echo "hooks on: tools/check.sh runs before each commit"
