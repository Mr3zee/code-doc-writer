# code-doc-writer

A skill for coding agents. It writes and rewrites doc comments, inline
code comments, user-facing messages, and documentation such as README
files, changelogs, and guides, in short plain technical English.
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

Or, into `~/.claude/skills/`:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/claude_install.sh | sh
```

Or, into `.claude/skills/` of the current directory:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/claude_install.sh | sh -s -- --project
```

### Codex

```
codex plugin marketplace add Mr3zee/code-doc-writer
codex plugin add code-doc-writer@code-doc-writer
```

Or, into `~/.agents/skills/`:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/codex_install.sh | sh
```

Or, into `.agents/skills/` of the current directory:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/codex_install.sh | sh -s -- --project
```

### pi

Add `-l` for the current project only:

```
pi install git:github.com/Mr3zee/code-doc-writer
```

Or, into `~/.agents/skills/`:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/pi_install.sh | sh
```

Or, into `.agents/skills/` of the current directory:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/pi_install.sh | sh -s -- --project
```

### Junie

Into `~/.junie/skills/`:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/junie_install.sh | sh
```

Into `.junie/skills/` of the current directory:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/junie_install.sh | sh -s -- --project
```

## Tests

The lint has a test suite in `tests/`. Run it from the repository root:

```
python3 -m unittest discover tests
```

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

Junie has no marketplace yet. The install script is in `docs/`, which
GitHub Pages serves at `https://mr3zee.github.io/code-doc-writer/`. A push
to `master` updates the page.
