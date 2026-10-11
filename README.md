# code-doc-writer

A skill for coding agents. It writes and rewrites doc comments, inline
code comments, and user-facing messages in short plain technical English.
The language rules come from ASD-STE100 (Simplified Technical English),
adapted for programming.

## Project rules

A repository can add its own rules in `DOCS_GUIDELINE.md` at its root.
The skill reads that file first. Its rules win over the skill.

## Install

One script for each agent. Each installs for the current user. Add
`-s -- --project` after `sh` to install into the current project instead.

| Agent | Command |
|---|---|
| Claude Code | `curl -fsSL https://mr3zee.github.io/code-doc-writer/claude_install.sh \| sh` |
| Codex | `curl -fsSL https://mr3zee.github.io/code-doc-writer/codex_install.sh \| sh` |
| pi | `curl -fsSL https://mr3zee.github.io/code-doc-writer/pi_install.sh \| sh` |
| Junie | `curl -fsSL https://mr3zee.github.io/code-doc-writer/junie_install.sh \| sh` |

The scripts live in `docs/` and GitHub Pages serves them from
<https://mr3zee.github.io/code-doc-writer/>. With the agent's CLI on the
PATH, a script installs through the agent's own marketplace or package
command. Without it, the script copies the skill folder into the agent's
skills directory.

### By hand

Claude Code. This repository is a plugin and a one-plugin marketplace:

```
claude plugin marketplace add Mr3zee/code-doc-writer
claude plugin install code-doc-writer@code-doc-writer
```

Or copy `skills/code-doc-writer` into `.claude/skills/` of a project or
into `~/.claude/skills/`.

Codex. This repository is a Codex plugin and a one-plugin marketplace:

```
codex plugin marketplace add Mr3zee/code-doc-writer
codex plugin add code-doc-writer@code-doc-writer
```

Or copy the skill folder into `.agents/skills/` of a project or into
`~/.agents/skills/`.

pi. Install the repository as a pi package. Add `-l` for the current
project only:

```
pi install git:github.com/Mr3zee/code-doc-writer
```

pi also reads `.agents/skills/` and `~/.agents/skills/`. The skill then
appears as `/skill:code-doc-writer`.

Junie. Copy the skill folder into `.junie/skills/` of a project or into
`~/.junie/skills/`. Junie also reads `.agents/skills/` and
`~/.agents/skills/`. Check it with `/skills` in Junie.

## Publish

### Claude Code marketplace

The marketplace file is `.claude-plugin/marketplace.json`. Its one entry
points at the repository root. To publish:

1. Run `claude plugin validate .` in the repository root.
2. Push the repository to GitHub.
3. Tell users to run `claude plugin marketplace add Mr3zee/code-doc-writer`.

To list the plugin in Anthropic's directory, follow the submission steps
on the Claude Code plugins documentation site.

### Codex

The marketplace file is `.agents/plugins/marketplace.json`, and the plugin
manifest is `plugin.json` at the root, with `.codex-plugin/plugin.json` as
the fallback for older Codex versions. Codex discovers the skill from
`skills/`. Push the repository and tell users to run
`codex plugin marketplace add Mr3zee/code-doc-writer`.

### pi

Publish the repository to npm with the `pi-package` keyword that
`package.json` already has. The package then appears in the pi package
gallery, and users run `pi install npm:code-doc-writer`.

### Junie

Junie has no marketplace yet. The install script lives in `docs/`, which
GitHub Pages serves at `https://mr3zee.github.io/code-doc-writer/`. A push
to `master` updates the page.
