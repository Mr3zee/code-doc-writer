#!/bin/sh
# Installs the code-doc-writer skill for Junie.
#
# User scope (default):   curl -fsSL https://mr3zee.github.io/code-doc-writer/junie_install.sh | sh
# Project scope:          curl -fsSL https://mr3zee.github.io/code-doc-writer/junie_install.sh | sh -s -- --project
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
  copy_skill "$(pwd)/.junie/skills"
else
  copy_skill "$HOME/.junie/skills"
fi
echo "Check it with /skills in Junie."
