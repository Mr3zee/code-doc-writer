#!/bin/sh
# Installs the code-doc-writer skill for Claude Code.
#
# User scope (default):   curl -fsSL https://mr3zee.github.io/code-doc-writer/claude_install.sh | sh
# Project scope:          curl -fsSL https://mr3zee.github.io/code-doc-writer/claude_install.sh | sh -s -- --project
#
# With the claude CLI on the PATH, the script installs the plugin from the
# marketplace. Without it, the script copies the skill folder.
set -eu

REPO="https://github.com/Mr3zee/code-doc-writer"

copy_skill() {
  target="$1"
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  curl -fsSL "$REPO/archive/refs/heads/master.tar.gz" | tar -xz -C "$tmp"
  mkdir -p "$target"
  rm -rf "$target/code-doc-writer"
  cp -R "$tmp"/code-doc-writer-master/skills/code-doc-writer "$target/"
  echo "Installed code-doc-writer into $target"
}

if [ "${1:-}" = "--project" ]; then
  copy_skill "$(pwd)/.claude/skills"
elif command -v claude >/dev/null 2>&1; then
  claude plugin marketplace add Mr3zee/code-doc-writer
  claude plugin install code-doc-writer@code-doc-writer
else
  copy_skill "$HOME/.claude/skills"
fi
echo "Check it with /plugin or by asking Claude Code to rewrite a comment."
