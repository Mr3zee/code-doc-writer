#!/bin/sh
# Installs the code-doc-writer skill for Junie.
#
# User scope (default):   curl -fsSL https://mr3zee.github.io/code-doc-writer/junie_install.sh | sh
# Project scope:          curl -fsSL https://mr3zee.github.io/code-doc-writer/junie_install.sh | sh -s -- --project
set -eu

REPO="https://github.com/Mr3zee/code-doc-writer"
TARGET="$HOME/.junie/skills"
if [ "${1:-}" = "--project" ]; then
  TARGET="$(pwd)/.junie/skills"
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

curl -fsSL "$REPO/archive/refs/heads/master.tar.gz" | tar -xz -C "$TMP"
mkdir -p "$TARGET"
rm -rf "$TARGET/code-doc-writer"
cp -R "$TMP"/code-doc-writer-master/skills/code-doc-writer "$TARGET/"

echo "Installed code-doc-writer into $TARGET"
echo "Check it with /skills in Junie."
