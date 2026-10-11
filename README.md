# code-doc-writer

A skill for coding agents. It writes and rewrites doc comments, inline
code comments, and user-facing messages in short plain technical English.
The language rules come from ASD-STE100 (Simplified Technical English),
adapted for programming.

The skill is in `skills/code-doc-writer/`:

- `SKILL.md`: the rules and the procedure.
- `references/ste-rules.md`: the STE rules in short form.
- `references/words.md`: the word list adapted for programming.
- `references/examples.md`: before and after pairs.
- `scripts/doc_lint.py`: a lint for comments in any language and for
  strings in JSON files.
- `scripts/code_unchanged.py`: checks that a rewrite changed comments only.

The folder follows the common Agent Skills layout: a directory with a
`SKILL.md` file. Claude Code, Codex, pi, and Junie all read that layout.

## Project rules

A repository can add its own rules in `DOCS_GUIDELINE.md` at its root.
The skill reads that file first. Its rules win over the skill.

## Install

### Claude Code

This repository is a plugin and a one-plugin marketplace. Add it and
install the plugin:

```
claude plugin marketplace add Mr3zee/code-doc-writer
claude plugin install code-doc-writer@code-doc-writer
```

Replace `Mr3zee` with the GitHub owner once the repository is pushed. A
local checkout works the same way with a path instead of `Mr3zee/<repo>`.
Inside a session, `/plugin marketplace add` and `/plugin install` do the
same.

Without the marketplace, copy `skills/code-doc-writer` into
`.claude/skills/` of a project or into `~/.claude/skills/`.

### Codex

This repository is a Codex plugin and a one-plugin marketplace
(`.agents/plugins/marketplace.json`). Add it and install the plugin:

```
codex plugin marketplace add Mr3zee/code-doc-writer
codex plugin add code-doc-writer@code-doc-writer
```

Without the marketplace, copy the skill folder into `.agents/skills/` of
a project or into `~/.agents/skills/`:

```
git clone https://github.com/Mr3zee/code-doc-writer
cp -r code-doc-writer/skills/code-doc-writer ~/.agents/skills/
```

### pi

Install the repository as a pi package. `package.json` declares the
`skills` folder:

```
pi install git:github.com/Mr3zee/code-doc-writer
```

Add `-l` to install for the current project only. The skill then appears
as `/skill:code-doc-writer`. pi also reads `.agents/skills/` and
`~/.agents/skills/`, so the Codex copy above works for pi too.

### Junie

Run the install script from the project page. User scope:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/junie_install.sh | sh
```

Project scope, from the project root:

```
curl -fsSL https://mr3zee.github.io/code-doc-writer/junie_install.sh | sh -s -- --project
```

The script copies the skill folder into `~/.junie/skills/` or
`.junie/skills/`. Junie also reads `.agents/skills/` and
`~/.agents/skills/`. Check the skill with `/skills` in Junie.

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

## Sources

- Claude Code: <https://code.claude.com/docs/en/plugins/create-marketplace>
- Codex: <https://developers.openai.com/codex/plugins/build>
- pi: <https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/packages.md>
- Junie: <https://junie.jetbrains.com/docs/agent-skills.html>
