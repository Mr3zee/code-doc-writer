# Maintenance

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
the fallback for older Codex versions. Codex finds the skill in
`skills/`. Push the repository and tell users to run
`codex plugin marketplace add Mr3zee/code-doc-writer`.

### pi

Publish the repository to npm with the `pi-package` keyword that
`package.json` already has. The package then appears in the pi package
gallery, and users run `pi install npm:code-doc-writer`.

### Junie

Junie has no marketplace yet. The install script is in `docs/`, which
GitHub Pages serves at `https://mr3zee.github.io/code-doc-writer/`. A push
to `master` deploys the page.
