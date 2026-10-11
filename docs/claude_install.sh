#!/bin/sh
# Installs the code-doc-writer skill for Claude Code.
#
# Into `~/.claude/skills`:
#     curl -fsSL https://mr3zee.github.io/code-doc-writer/claude_install.sh | sh
# Into `.claude/skills` of the current directory:
#     curl -fsSL https://mr3zee.github.io/code-doc-writer/claude_install.sh | sh -s -- --project
set -eu

REPO="https://github.com/Mr3zee/code-doc-writer"
if [ "${1:-}" = "--project" ]; then
  TARGET="$(pwd)/.claude/skills"
else
  TARGET="$HOME/.claude/skills"
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

curl -fsSL "$REPO/archive/refs/heads/master.tar.gz" | tar -xz -C "$TMP"
mkdir -p "$TARGET"
rm -rf "$TARGET/code-doc-writer"
cp -R "$TMP"/code-doc-writer-master/skills/code-doc-writer "$TARGET/"

echo "Installed code-doc-writer into $TARGET"
echo "To check it, ask Claude Code to rewrite a comment."
