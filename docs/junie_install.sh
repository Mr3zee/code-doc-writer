#!/bin/sh
# Installs the code-doc-writer skill for Junie.
#
# Into `~/.junie/skills`:
#     curl -fsSL https://mr3zee.github.io/code-doc-writer/junie_install.sh | sh
# Into `.junie/skills` of the current directory:
#     curl -fsSL https://mr3zee.github.io/code-doc-writer/junie_install.sh | sh -s -- --project
set -eu

REPO="https://github.com/Mr3zee/code-doc-writer"
if [ "${1:-}" = "--project" ]; then
  TARGET="$(pwd)/.junie/skills"
else
  TARGET="$HOME/.junie/skills"
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

curl -fsSL "$REPO/archive/refs/heads/master.tar.gz" | tar -xz -C "$TMP"
mkdir -p "$TARGET"
rm -rf "$TARGET/code-doc-writer"
cp -R "$TMP"/code-doc-writer-master/skills/code-doc-writer "$TARGET/"

echo "Installed code-doc-writer into $TARGET"
echo "Check it with /skills in Junie."
