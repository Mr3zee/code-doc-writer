#!/bin/sh
# Installs the code-doc-writer skill for pi.
#
# User scope (default):   curl -fsSL https://mr3zee.github.io/code-doc-writer/pi_install.sh | sh
# Project scope:          curl -fsSL https://mr3zee.github.io/code-doc-writer/pi_install.sh | sh -s -- --project
#
# With the pi CLI on the PATH, the script installs the repository as a pi
# package. Without it, the script copies the skill folder.
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

if command -v pi >/dev/null 2>&1; then
  if [ "${1:-}" = "--project" ]; then
    pi install -l git:github.com/Mr3zee/code-doc-writer
  else
    pi install git:github.com/Mr3zee/code-doc-writer
  fi
elif [ "${1:-}" = "--project" ]; then
  copy_skill "$(pwd)/.agents/skills"
else
  copy_skill "$HOME/.agents/skills"
fi
echo "Check it with /skill:code-doc-writer in pi."
