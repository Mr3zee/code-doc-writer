#!/bin/sh
# Installs the code-doc-writer skill for Codex.
#
# User scope (default):   curl -fsSL https://mr3zee.github.io/code-doc-writer/codex_install.sh | sh
# Project scope:          curl -fsSL https://mr3zee.github.io/code-doc-writer/codex_install.sh | sh -s -- --project
#
# With the codex CLI on the PATH, the script installs the plugin from the
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
  copy_skill "$(pwd)/.agents/skills"
elif command -v codex >/dev/null 2>&1; then
  codex plugin marketplace add Mr3zee/code-doc-writer
  codex plugin add code-doc-writer@code-doc-writer
else
  copy_skill "$HOME/.agents/skills"
fi
echo "Restart Codex if the skill does not appear."
