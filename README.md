# code-doc-writer

A skill for coding agents. It writes and rewrites doc comments, inline
code comments, and user-facing messages in short plain technical English.
The language rules come from ASD-STE100 (Simplified Technical English),
adapted for programming.

## Project rules

A repository can add its own rules in `DOCS_GUIDELINE.md` at its root.
The skill reads that file first. Its rules win over the skill.

## Install

### Claude Code

```
claude plugin marketplace add Mr3zee/code-doc-writer
claude plugin install code-doc-writer@code-doc-writer
```

Or:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/claude_install.sh | sh
```

The script saves the skill into `~/.claude/skills/`. With `sh -s -- --project` it saves
into `.claude/skills/` of the current directory instead.

### Codex

```
codex plugin marketplace add Mr3zee/code-doc-writer
codex plugin add code-doc-writer@code-doc-writer
```

Or:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/codex_install.sh | sh
```

The script saves the skill into `~/.agents/skills/`. With `sh -s -- --project` it saves
into `.agents/skills/` of the current directory instead.

### pi

Add `-l` for the current project only:

```
pi install git:github.com/Mr3zee/code-doc-writer
```

Or:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/pi_install.sh | sh
```

The script saves the skill into `~/.agents/skills/`. With `sh -s -- --project` it saves
into `.agents/skills/` of the current directory instead.

### Junie

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/junie_install.sh | sh
```

The script saves the skill into `~/.junie/skills/`. With `sh -s -- --project` it saves
into `.junie/skills/` of the current directory instead.

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
