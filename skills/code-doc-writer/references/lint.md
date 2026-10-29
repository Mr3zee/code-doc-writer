# Lint

The lint finds punctuation, the words in `words.md`, a
sentence over the limit, a likely passive, an "-ing" clause, a relative
clause, and an uncontracted negative. Nothing else.

What the lint doesn't check:

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

Three soft warnings are questions about the use, not the word.
`figurative?` marks a word that often has a figurative meaning. `speaks?`
marks a speech or thought verb. The verb passes when a person is the
actor: "Tell the user to run the task". It fails when code or a text is
the actor: "The API tells the caller". `clause?` marks "whose" and
", which", the words that open a clause inside a noun phrase. The clause
passes in a sentence: "The task, which runs last, writes the report" is
one sentence with an aside. It fails in a list item or a one-line doc
that is a noun phrase: "An option whose default is off" is a sentence in
the shape of a noun phrase. The lint doesn't mark "that" or a bare
"which". Both are often plain pronouns.

What the lint reads in each kind of file:

| File | Reads | Skips |
|---|---|---|
| `.md`, `.markdown`, `.mdx` | Every paragraph, heading, list item, table row, front matter value, and link text. A link counts as one word. Every finding is a soft warning, because the lint can't separate prose from unknown markup. | Code blocks, HTML tags, HTML comments, images, template calls, and link reference definitions. |
| `.json` | Every string value that has a space in it. | Identifiers, paths, and URLs. |
| Source | The `/* */`, `//`, and `#` comments and the triple-quoted strings. | String literals. |

To lint a string literal, one message, or a text in another doc format,
put the text in a temporary `.md` file and lint that file.
