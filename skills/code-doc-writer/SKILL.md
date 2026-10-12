---
name: code-doc-writer
description: >-
  Write or rewrite every text a person reads in code or in documentation,
  in short plain technical English based on ASD-STE100. Use lists and
  tables where the facts have a structure. The texts are doc comments (KDoc, Javadoc, JSDoc, Doxygen, docstrings, XML docs,
  rustdoc, Go doc comments), inline comments, TODO and FIXME notes,
  user-facing messages (diagnostics, errors, exceptions, assertions,
  warnings, deprecation notices, log lines, CLI output, help text,
  message templates), and documentation in any format (README files,
  changelogs, docs websites, guides, Markdown, reStructuredText,
  AsciiDoc). Use it every time you write, change, or delete such a text,
  in any language, during any task. A one-line comment that is a side
  effect of a code change counts. Also use it when someone asks to
  simplify, shorten, clean up, review, or remove the noise or the
  bullshit from docs, comments, or messages. Use it when someone asks for
  STE, Simplified Technical English, or more readable English or language.
---

# Code doc writer

Write every text that a person reads, in code or in documentation, so
the reader gets the facts fast. Three kinds of rules:

- Language rules: ASD-STE100 (Simplified Technical English), adapted for
  programming.
- Scope rules: a text holds only what the reader needs in this place and
  doesn't already have.
- Form rules: structured text where the facts have a structure. Sentences
  and paragraphs where they don't.

The measure: the text that gives the facts in the fewest words, in the
form that the reader scans fastest, is the best text.

## Scope

A rewrite follows the same rules as a new text. A one-line comment that
is a side effect of a code change counts.

| Text | Examples |
|---|---|
| Doc comments | KDoc, Javadoc, JSDoc, Doxygen, docstrings, XML docs, rustdoc, Go doc comments. |
| Inline comments | `//`, `#`, and `/* */` comments, TODO and FIXME notes. |
| Comments in data files | A `$comment` key in JSON, a `#` line in YAML, a comment block in a template. |
| User-facing messages | Diagnostics, errors, exceptions, assertions, warnings, deprecation notices, log lines, CLI output, help text, message templates in data files. |
| Documentation | README files, changelogs, guides, docs websites, Markdown, reStructuredText, AsciiDoc, any other doc format. |

Rules for every kind of text:

- The skill applies to the text, not the code. When you write code, the
  skill applies to the comments and messages you write with it.
- Keep the syntax of the format: the comment syntax of the language and
  the markup of the doc format. Keep the links, references, tags, and
  placeholders that a tool reads, such as `@see`, `[Name]`, `{@link}`,
  `{0}`.
- When the task is a rewrite, change text only: no code, imports,
  annotations, placeholders, or code formatting.
- A task that names only the comments of a file still covers the messages
  in that file. "Don't change the code" means the logic. A message string
  is text, not logic.
- A generated file gets its text from a template. Edit the template.

## Two readers

Every text has one of two readers. Decide which one before you write.

| | User docs | Private docs |
|---|---|---|
| Reader | A user of the product or library. Knows the domain, but doesn't read the source. | A developer of this codebase. Knows the domain, the modules, and the code. |
| Has | One place at a time: the website, the README, the doc comment in the IDE, or one overload of a function. | The source and the user docs. |
| Tell | What it does. When to use it. How to use it. What the reader must know first. | Only what the code can't show. |
| Repeat | Every fact the reader needs in this place, even when another page, the README, or another overload also states it. | A fact from the user docs only to add to it. |
| Never | Implementation, internal types, other modules, build tooling, history, design arguments. | What the code already shows. What the user docs already say. History. |

Which reader a text has:

| Text | Reader |
|---|---|
| Documentation that the project publishes: a website, a README, a guide, a changelog, help text. | User docs. |
| Documentation that only the developers of this codebase read: a design note, an internal wiki page, a comment in a data file, all comments in test code or data. | Private docs. |
| A doc comment on a declaration that a user of the published artifact can see. | User docs. Visibility alone doesn't decide. A public class in a module that users never depend on has private docs. Check the module's purpose before you decide. |
| A doc comment on any other declaration. | Private docs. |
| An inline comment. | Private docs. |
| A message. | User docs. The reader has the message and nothing else. |

Use `@see` or a link for related API or a docs page, not for a fact the
reader must know.

## Procedure

1. Read `DOCS_GUIDELINE.md` in the repository root if it exists. It holds
   the project's terms, link formats, required tags, page shapes, and
   exceptions. The rules in that file override this skill.
2. Read the source of the facts first: the code, the existing text, the
   spec. For a declaration, read the signature, the body, and the callers
   when the purpose isn't clear.
3. Draft the text: one sentence for each fact that the reader needs. In a
   rewrite, the draft is the existing text, split into sentences.
4. Apply the keep test to each sentence. Delete or keep.
5. Write each kept sentence with the language rules.
6. Give the kept sentences their form: a list or a table when
   [Form](#language-rules) says so, in the order that the shape of the
   text gives. [Shape of a document](#shape-of-a-document), [Comments in
   code](#comments-in-code), and [Messages](#messages) give the shapes.
7. Check each claim against the code or the project's docs. Fix a wrong
   claim. Find the fact behind an ambiguous sentence and write it. When
   you can't check a claim that comes from the original text, keep its
   wording.
8. Run `scripts/doc_lint.py` on the file. Fix every hard failure. Read
   each soft warning and fix it or leave it with a reason. [Lint](#lint)
   tells what the lint finds and what it can't see.
9. In a rewrite, compare the result with the original. The result has
   every kept fact and invents none. A qualifier such as "some", "only",
   or "when X" is a fact.
10. Read the result as the reader. This step, not the lint, decides
    whether the text is complete. Delete a sentence that doesn't change what
    the reader does or knows. Readability is the measure, and a shorter
    text with the same facts reads faster. When the result is close to
    the original in length, do the keep test again.
11. After each self-contained part (a file, a page, a section, a group of
    related declarations), read the result once more for:
    - A sentence that referred to a deleted sentence.
    - A link to a deleted section.
    - A term that the rest of the file no longer uses.
    - A fact that now appears twice.
    - A text that no longer matches the code or the behavior it describes.

Two rules on style:

- The style of the request doesn't change the style of the text. A casual
  or blunt request still gets a plain technical text.
- Your report to the person follows the same language and form rules.

## Keep test

Delete a sentence when one of these is true:

- The context already says it: the name, the type, the signature, the
  modifier, the heading, the previous sentence, or the example. One
  exception: user docs state the default value.
- In private docs: another text that the reader has already says it. Keep
  the fact in one place. Link to that place.
- It explains a reason to a reader who already knows the domain.
- It teaches the host language, tool, or platform instead of this
  product. How to declare a dependency, what `this` is in a block, how
  a language feature works, how a version control system works.
- It tells history, intent, or feelings and nothing else. "Previously",
  "used to", and "now" belong to version control. Delete the intent word
  first ("deliberately", "on purpose", "honest", "intended", "we chose").
  Then apply the keep test to the fact that remains.
- It describes what other parts of the system do with this element. For
  user docs this is always a delete. For private docs, keep it only when
  a search for the name doesn't find the other part.
- It gives a second example of the same thing.

Keep a sentence when one of these is true:

- A reader can do the wrong thing without it. Such a fact is a
  precondition, a side effect, thread safety, ownership, an order of steps
  or calls, a limit, or a unit.
- It tells a user when to use the element. When the original gives no
  real condition, take one from the project's docs or keep the original.
  Never infer a condition from the rationale.
- It gives a constraint from outside: a tool bug, a protocol, a version
  limit, a file format. Give the source of the constraint. A workaround
  has to have a bug link. When the text has none, add it.
- It gives the one invariant that the code relies on and doesn't check.
- It tells why the code or the procedure doesn't do the obvious thing.

After the test:

- When a delete rule and a keep rule both match a sentence, the keep rule
  wins.
- Add a fact that the draft lacks only when the source proves it and the
  reader needs it. Such a fact is what happens on misuse, the error or
  diagnostic that the code reports, or the exception it throws.
- State a default that is the same for a group of elements once, on the
  group, not on each member.
- When the test deletes every sentence, delete the whole text.
- When the project requires a doc comment on every public declaration,
  keep one sentence. It says what the declaration is for, not its name
  again.

## Language rules

`references/ste-rules.md` gives the ASD-STE100 source of the rules that
come from the standard.

Form:

- Prefer structured text to sentences and paragraphs. A paragraph is for
  one fact, or for a line of argument where each sentence follows from
  the one before.
- A vertical list for three or more parallel items: steps, options,
  conditions, parts, rules. Two items can stay in one sentence.
- A table when three or more items have the same two or more attributes:
  option and default, mode and effect, reader and rule.
- A numbered list when the order matters. A bulleted list when it
  doesn't.
- A lead-in sentence names what the list holds and ends with a colon.
- One item holds one fact, in a noun phrase or in one to three sentences.
  All items of a list have the same grammar: all noun phrases, all
  sentences, or all commands.
- Put the label first in an item that has one: "`fast`: syntax checks
  only." Don't repeat the lead-in words in each item.
- Nest a list one level at most. Put more structure in a table or a
  section.
- Use the list and table syntax that the format renders: Markdown in
  Markdown docs, KDoc, JSDoc, and rustdoc, HTML in Javadoc, the markup of
  the docstring tool in Python, the directives of reStructuredText and
  AsciiDoc. When no tool renders the text, write one item on each line
  with a hyphen.
- A message, a log line, and a one-fact inline comment stay in
  sentences.

Sentences:

- Aim for at most 20 words in an instruction and 25 in a description. A
  code span, a link, a number, a placeholder, or a parenthesis counts as one
  word. The lint counts the same way. When a split makes the sentence
  harder to read, or removes a fact, keep the long sentence.
- One topic in each sentence. One instruction in each sentence. A cause and
  its effect are one topic: keep them in one sentence with "because" or
  "so". Two facts that only stand next to each other get two sentences.
- Active voice. Name the actor: the function, the caller, the compiler, the
  task, the user. Use the passive only when the actor is unknown.
- Present tense for behavior. "Returns the size", not "will return".
- A description describes. Use the imperative only in a sentence that
  tells the reader what to do: "Call `close` after use."
- Condition or reason first, then the instruction. "If the file is missing,
  the task fails." "The getter is deprecated, so read it with reflection."
  One exception: a warning about a harmful action starts with the command,
  then the risk. "Don't call this from the UI thread. It blocks until the
  file is read."
- Keep articles and the word "that". "Make sure that the list is sorted."
- No semicolons. No dashes for asides. Parentheses only for a reference,
  an identifier, an abbreviation, a short explanation, or an alternative
  (STE 8.3).
- No "-ing" clauses. "When you add a check", not "when adding a check".
  "A change breaks users", not "without breaking users".
- A paragraph has at most six sentences and one topic.

Words:

- Use the plain verb: "use", not "utilize". "Get", not "retrieve".
  `references/words.md` has the table of swaps.
- One term for one thing. Pick a name and use it everywhere in the module
  or the page.
- Technical nouns and verbs of the domain stay. Identifiers, tool names,
  and the domain's own verbs (compile, resolve, register, publish,
  serialize, fall back) are the exact words. Don't replace them with a
  plain verb that is less exact.
- No idioms, metaphors, or personification. Each word has its literal
  meaning only. "A bakes its logic into B" is wrong. "The oven bakes the bread"
  is literal. Say the plain fact: "A stores the value at construction."
  `references/words.md` lists the words that are often figurative. A word
  that looks figurative but has a technical meaning in the domain stays:
  catch an exception, pin a version.
- "Keep" means "don't remove". It doesn't state a requirement or a state.
  "A workaround has to have a bug link", not "a workaround keeps its bug
  link". "The list has one entry", not "the list keeps one entry".
- No filler: "note that", "simply", "in order to". `references/words.md`
  has the list.
- No Latin abbreviations. "For example", not "e.g.". "That is", not
  "i.e.". Delete "etc." and name the items or stop the list.
- No hedge modals. "May", "might", "could", "would" become "can". Replace
  "should" with "must" or delete it. A modal that marks a condition is a
  fact: "may write" becomes "can write", never "writes".
- American spelling.
- Use the common negative contractions: can't, don't, doesn't, isn't,
  won't, didn't, aren't, wasn't. Never "cannot".
- A link names what it points to, not the act of reading. Not "See the
  documentation". Write "[Request timeouts](url)". Use `@see` with a name
  when the doc tool renders one. When the tool renders no name, a bare URL
  in `@see` is the accepted form.

## Shape of a document

- Follow the shape of the existing pages of the same kind.
- One topic in each section. The headings alone give the outline.
- The common case comes before the exceptions. A rule comes before the
  example that shows it.
- A changelog entry says what changed for the reader, not what changed in
  the code.

## Comments in code

Decide the reader first. [Two readers](#two-readers) tells which
declarations have user docs.

- First sentence: what it is or what it does, in words the name doesn't
  already give. A function starts with its action: "Returns", "Registers",
  "Writes". A type or property starts with a noun phrase: "The timeout of
  each request." When the name gives every fact, write no comment. Never
  start with "Also".
- Then the facts from the keep test. One sentence each, or a list or a
  table when [Form](#language-rules) says so.
- A code example when it shows the reader how to use the declaration
  faster than words do. The example is short and has no comments inside
  it. For more examples, link to the website.
- Tags, in this order:
  - `@param` only when the name and the type don't say it. A `@param` in
    user docs gets one short sentence even when the doc of the type gives
    the long form, because the reader opens one declaration at a time.
  - `@return` only when the first sentence doesn't say it.
  - `@throws` when the caller can catch or check for the exception. An
    argument or configuration error that stops the program gets no tag.
- Most doc comments fit in one to three sentences.
- A one-line doc on a member of a group can be a noun phrase: "The timeout
  of `read`." A noun phrase has no verb, so the sentence rules don't apply
  to it.
- An inline comment describes. "The pair maps to one `\n`, so an
  insertion can't split it." Not "Map the pair to one `\n`". Use the
  imperative only for an instruction to the next editor, with the reason
  first: "The getter has a side effect in library version 2.4, so don't
  read it."
- Delete a comment that says what the next lines do. The code shows it.
  This includes a comment that names the algorithm: "binary search",
  "lower bound", "iterate over the handlers".
- Put the comment where the decision is.
- Three or more parallel facts, such as the cases of a branch, go in a
  list with one item on each line.

## Messages

A message has three parts, in this order:

1. The problem. Name the element with its exact identifier. One or two
   sentences.
2. The fix. One sentence in the imperative. "Add a return type to
   `parse`."
3. A reference, when more detail exists elsewhere. Better as a link.

Rules for messages:

- Search the file for string literals that a person reads.
- In a message every sentence, the problem included, gets the 20-word
  limit of an instruction. Lint the messages with `--max-words 20`.
- The line length limit of the code doesn't apply to a message in a data
  file.
- At most three sentences for the problem and the fix. A fixed closing
  sentence that every message of a kind carries, such as a suppression
  hint, is one short sentence after them and isn't counted.
- The fix ends the message body. No reason after it. Alternative fixes
  join in one sentence with "or".
- No blame, no jokes, no "oops", no "please", no exclamation marks.
- Present tense. "The class is open", not "the class has been left open".
- A log line states one event with its identifiers. It has no filler and
  no advice.

Before:

```
The configuration file `{0}` could not be loaded because it appears to
contain one or more entries whose keys aren't recognized by this version
of the tool, which is why processing has been aborted. Please double-check
the file and try again!
```

After:

```
`{0}` has a key that this version of the tool doesn't accept. Remove the
key, or update the tool.
```

## Examples

Before (a rationale and a history):

```
The `strict` option, which is turned off by default because we found that
most users were overwhelmed by the volume of warnings when it was first
introduced, makes the tool treat every warning as an error, which is
useful in CI pipelines where you want the build to fail early rather than
let problems accumulate over time.
```

After:

```
`strict` treats every warning as an error. Use it in CI. Default is off.
```

Before (an intent and a reader who knows the domain):

```
We deliberately keep the index outside the output directory. The packaging
step zips everything in the output directory, and an index inside the
archive would be picked up by the loader as a plugin, which is obviously
not what we want. The index is regenerated on every run anyway, so it can
never go stale.
```

After:

```
The index isn't in the output directory: the packaging step zips that
directory, and the loader treats each file in the archive as a plugin.
Every run regenerates the index.
```

Before (parallel facts in a paragraph):

```
The `fast` mode runs only the syntax checks and takes about a second. The
`full` mode also runs the type checks and takes about a minute. The `ci`
mode is `full` plus the lint, and it fails on a warning.
```

After:

```
The check runs in one of three modes:

- `fast`: syntax checks only. About a second.
- `full`: syntax and type checks. About a minute.
- `ci`: `full` and the lint. Fails on a warning.
```

Before (parallel facts with the same attributes):

```
The `timeout` option sets how long a request waits, in seconds, and
defaults to 30. The `retries` option sets how many times a failed request
runs again and defaults to 3. The `verbose` option prints each request
and is off by default.
```

After:

```
| Option | Effect | Default |
|---|---|---|
| `timeout` | Seconds that a request waits. | 30 |
| `retries` | Runs of a failed request after the first. | 3 |
| `verbose` | Prints each request. | off |
```

Before (restates the context), under the heading "Configuration options":

```
This section describes the configuration options.
```

After: no text. The heading says it.

`references/examples.md` has more pairs: documentation pages, doc
comments, inline comments, docstrings, messages, and log lines.

## Lint

The lint finds punctuation, the words in `references/words.md`, a
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

## Final check

- Every sentence passed the keep test.
- No user doc names a private type, a module, a build tool, or an
  internal mechanism.
- User docs state defaults and tell when to use the element.
- Each term has one name in the file.
- No fact appears twice in the file.
- No idiom, no filler, no Latin abbreviation, no semicolon, no dash aside.
- Three or more parallel facts are a list or a table, not a paragraph.
- In a rewrite task, the code didn't change. Diff the file: each changed
  line is a comment, a message string, or documentation.
- The lint reports no hard failure, and each soft warning has an answer.
