# Lint

The lint finds punctuation, the words in `words.md`, a
sentence over the limit, a likely passive, an "-ing" clause, and an
uncontracted negative. Nothing else.

What the lint can't see:

- A sentence that fails the keep test.
- A fact stated twice.
- A reason given to a reader who knows it.
- A figurative use of a word that isn't in the list.
- An ambiguous sentence.
- A passive with a contracted verb.
- A wrong claim about the code.
- A paragraph that has to be a list or a table.

These items are most of the rules. You find them only when you read the
text as the reader. Apply the rules first, then run the lint. Never
report a clean lint as the result of the skill.

```
python3 scripts/doc_lint.py [--json] [--max-words N] FILE...
```

| Finding | Exit code | What it is |
|---|---|---|
| Hard failure | 1 | A semicolon, an em dash, an en dash, a double hyphen, or a hyphen with a space on each side. |
| Soft warning | 0 | Every other finding. A question, not an order. |

What the lint reads in each kind of file:

| File | Reads | Skips |
|---|---|---|
| `.md`, `.markdown`, `.mdx` | Every paragraph, heading, list item, table row, front matter value, and link text. A link counts as one word. Every finding is a soft warning, because the lint can't tell prose from markup it doesn't know. | Code blocks, HTML tags, HTML comments, images, template calls, and link reference definitions. |
| `.json` | Every string value that has a space in it. | Identifiers, paths, and URLs. |
| Source | The `/* */`, `//`, and `#` comments and the triple-quoted strings. | String literals. |

To lint a string literal, one message, or a text in another doc format,
put the text in a temporary `.md` file and lint that file.
