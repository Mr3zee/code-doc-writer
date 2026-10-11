#!/bin/sh
# Installs the code-doc-writer skill for Codex.
#
# Into `~/.agents/skills`:
#     curl -fsSL https://mr3zee.github.io/code-doc-writer/codex_install.sh | sh
# Into `.agents/skills` of the current directory:
#     curl -fsSL https://mr3zee.github.io/code-doc-writer/codex_install.sh | sh -s -- --project
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
echo "If the skill doesn't appear, restart Codex."
