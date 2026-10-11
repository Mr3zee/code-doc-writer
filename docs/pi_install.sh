#!/bin/sh
# Copies the code-doc-writer skill into the skills directory of pi.
#
# User scope (default):   curl -fsSL https://mr3zee.github.io/code-doc-writer/pi_install.sh | sh
# Project scope:          curl -fsSL https://mr3zee.github.io/code-doc-writer/pi_install.sh | sh -s -- --project
set -eu

REPO="https://github.com/Mr3zee/code-doc-writer"
if [ "${1:-}" = "--project" ]; then
  TARGET="$(pwd)/.agents/skills"
else
  TARGET="$HOME/.agents/skills"
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

curl -fsSL "$REPO/archive/refs/heads/master.tar.gz" | tar -xz -C "$TMP"
mkdir -p "$TARGET"
rm -rf "$TARGET/code-doc-writer"
cp -R "$TMP"/code-doc-writer-master/skills/code-doc-writer "$TARGET/"

echo "Installed code-doc-writer into $TARGET"
echo "Check it with /skill:code-doc-writer in pi."
