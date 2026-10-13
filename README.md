# code-doc-writer

A skill for coding agents. It writes and rewrites doc comments, inline
code comments, user-facing messages, pull request and issue
descriptions, and documentation such as README files, changelogs, and
guides. The text is short plain technical English.
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

## Update

### Claude Code

Claude Code doesn't update this plugin on its own. To turn auto-update on,
open `/plugin`, go to **Marketplaces**, select `code-doc-writer`, and enable
auto-update. Claude Code then loads a new version in the next session.

To update by hand:

```
claude plugin marketplace update code-doc-writer
claude plugin update code-doc-writer@code-doc-writer
```

Then restart Claude Code.

### Codex

Refresh the marketplace, then add the plugin again:

```
codex plugin marketplace upgrade
codex plugin add code-doc-writer@code-doc-writer
```

### pi

```
pi update --extension git:github.com/Mr3zee/code-doc-writer
```

### curl scripts

Run the same install command again. The script removes the old copy
and installs the current `master` branch.
