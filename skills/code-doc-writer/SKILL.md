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
  effect of a code change counts. Also use it when someone asks to cut
  the bullshit, simplify, shorten, clean up, remove the noise from, or
  review docs, comments, or messages, and when someone asks for STE or
  Simplified Technical English.
---

# Code doc writer

Write comments, messages, and documentation so a reader gets the facts
fast. Three kinds of rules:

- Language rules: ASD-STE100 (Simplified Technical English), adapted for
  programming.
- Scope rules: a comment is only for what the code can't show.
- Form rules: structured text where the facts have a structure. Sentences
  and paragraphs where they don't.

The measure: the text that gives the facts in the fewest words, in the
form that the reader scans fastest, is the best text.

## Scope

- Every doc comment, inline comment, and user-facing message that you write
  or change, during any task. A rewrite follows the same rules as a new
  text.
- User-facing messages are diagnostics, errors, exceptions, assertions,
  warnings, deprecation notices, log lines, CLI output, help text, and
  message templates in data files.
- A task that names only the comments of a file still covers the messages
  in that file. "Don't change the code" means the logic. A message string
  is text, not logic.
- Comments in data files are private docs: a `$comment` key in JSON, a `#`
  line in YAML, a comment block in a template.
- Any documentation: README files, changelogs, docs websites, guides,
  Markdown, reStructuredText, AsciiDoc, or any other doc format. The
  language and form rules apply as they are. For the scope rules, the doc
  is the reader's one place.
- The skill applies to the text, not the code. When you write code, the
  skill applies to the comments and messages you write with it. Keep the
  comment syntax of the language.
- When the task is a rewrite, change text only: no code, imports,
  annotations, placeholders, or code formatting.
- A generated file gets its text from a template. Edit the template.
- Keep the syntax of links, references, and tags that a tool reads, such
  as `@see`, `[Name]`, `{@link}`, `{0}`. [Shape of a doc
  comment](#shape-of-a-doc-comment) decides whether a `@param` or a
  `@throws` is there.

## Two readers

| | Public API docs | Private docs |
|---|---|---|
| Reader | A user of the library. Knows the domain, but doesn't read the source. | A developer of this codebase. Knows the domain and the modules. |
| Has | One place at a time: the website, the README, the doc comment in the IDE, or one overload of a function. | The source and the public docs. |
| Tell | What it does. When to use it. How to call it. What the caller must know. | Only what the code can't show. |
| Repeat | Every fact the reader needs in this place, even when the website, the README, or another overload also states it. | A public fact only to add to it. |
| Never | Implementation, internal types, other modules, build tooling, history, design arguments. | What the code already shows. What the public docs already say. History. |

Which column a declaration gets:

- Public API when a user of the published artifact can see the
  declaration.
- Visibility alone doesn't decide. A public class in a module that users
  never depend on has private docs.
- Check the module's purpose before you decide.
- Use `@see` for related API, not for a fact the caller must know.

## Procedure

1. Read `DOCS_GUIDELINE.md` in the repository root if it exists. It holds
   the project's terms, link formats, required tags, and exceptions. The
   rules in that file override this skill.
2. Read the code first. If the purpose isn't clear, read the signature,
   the body, and the callers.
3. Draft the text: one sentence for each fact that the reader needs. In a
   rewrite, the draft is the existing text, split into sentences.
4. Apply the keep test to each sentence. Delete or keep.
5. Write each kept sentence with the language rules.
6. Give the kept sentences their form: a list or a table when
   [Form](#language-rules) says so, in the order that [Shape of a doc
   comment](#shape-of-a-doc-comment) gives.
7. Check each claim about the code against the code or the project's
   docs. Fix a wrong claim. Find the fact behind an ambiguous sentence and
   write it. When you can't check a claim that comes from the original
   text, keep its wording.
8. Run `scripts/doc_lint.py` on the file. The lint is a complement to
   steps 4 to 7, never a replacement for them: it finds punctuation and
   listed words, and nothing else. Fix every hard failure. Read each soft
   warning and fix it or leave it with a reason. [Lint](#lint) tells what
   the lint reads and what it can't see.
9. In a rewrite, compare the result with the original. The result has
   every kept fact and invents none. A qualifier such as "some", "only",
   or "when X" is a fact.
10. Read the result as the reader. This step, not the lint, decides
    whether the text is complete. Delete a sentence that doesn't change what
    the reader does or knows. Readability is the measure, and a shorter
    text with the same facts reads faster. When the result is close to
    the original in length, do the keep test again.
11. After each self-contained part (a file, a class, a group of related
    declarations), read the result once more for:
    - A sentence that referred to a deleted sentence.
    - A link to a deleted section.
    - A term that the rest of the file no longer uses.
    - A fact that now appears twice.
    - A comment that no longer matches the code below it.

Two rules on style:

- The style of the request doesn't change the style of the text. A casual
  or blunt request still gets a plain technical comment.
- Your report to the person follows the same language and form rules.

## Keep test

Delete a sentence when one of these is true:

- The name, type, signature, or modifier already says it. One exception:
  a public doc states the default value.
- In private docs: another comment or the public doc already says it. Keep
  it in one place. Link to that place with a reference.
- It explains a reason to a reader who already knows the domain.
- It teaches the host language, tool, or platform instead of this
  declaration. How to declare a dependency, what `this` is in a block, how
  a language feature works.
- It tells history, intent, or feelings and nothing else. "Previously",
  "used to", and "now" belong to version control. Delete the intent word
  first ("deliberately", "on purpose", "honest", "intended", "we chose").
  Then apply the keep test to the fact that remains.
- It describes what other parts of the system do with this declaration.
  For public docs this is always a delete. For private docs, keep it only
  when a search for the name doesn't find the other part.
- It gives a second example of the same thing.

Keep a sentence when one of these is true:

- A caller can misuse the declaration without it: a precondition, a side
  effect, thread safety, ownership, order of calls, or a unit.
- It tells a public reader when to use the declaration. When the original
  gives no real condition, take one from the project's docs or keep the
  original. Never infer a condition from the rationale.
- It gives a constraint from outside the code: a tool bug, a protocol, a
  version limit, a file format. Give the source of the constraint. A
  workaround has to have a bug link. When the comment has none, add it.
- It gives the one invariant that the code relies on and doesn't check.
- It tells why the code doesn't do the obvious thing.

After the test:

- When a delete rule and a keep rule both match a sentence, the keep rule
  wins.
- Add a fact that the draft lacks only when the code proves it and a
  caller needs it. Such a fact is what happens on misuse, the error or
  diagnostic that the code reports, or the exception it throws.
- State a default that is the same for a group of declarations once, on
  the group or the class, not on each member.
- When the test deletes every sentence, delete the whole comment.
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
- Use the list and table syntax that the doc tool renders: Markdown in
  KDoc, JSDoc, rustdoc, and Markdown docs, HTML in Javadoc, the
  markup of the docstring tool in Python. When no tool renders the
  comment, write one item on each line with a hyphen.
- A message, a log line, and a one-fact inline comment stay in
  sentences.

Sentences:

- Aim for at most 20 words in an instruction and 25 in a description. A
  code span, a link, a number, a placeholder, or a parenthesis counts as one
  word. When a split makes the sentence harder to read, or removes a
  fact, keep the long sentence.
- One topic in each sentence. One instruction in each sentence. A cause and
  its effect are one topic: keep them in one sentence with "because" or
  "so". Two facts that only stand next to each other get two sentences.
- Active voice. Name the actor: the function, the caller, the compiler, the
  task. Use the passive only when the actor is unknown.
- Present tense for behavior. "Returns the size", not "will return".
- A doc on a type, a function, or a property describes. Use the imperative
  only in a sentence that tells the caller what to do: "Call `close` after
  use."
- Condition or reason first, then the instruction. "If the file is missing,
  the task fails." "The getter is deprecated, so read it with reflection."
  One exception: a warning about a harmful call starts with the command,
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

- Use the plain verb. Do, get, give, make, use, set, show, find, let, need,
  keep, put, start, stop, send, read, write, check, add, remove, change.
  `references/words.md` has the full table of swaps.
- One term for one thing. Pick a name and use it everywhere in the module.
- Technical nouns and verbs of the domain stay. Identifiers, tool names,
  and the domain's own verbs (compile, resolve, register, publish,
  serialize, fall back) are the exact words. Don't replace them with a
  plain verb that is less exact.
- No idioms, metaphors, or personification. Each word has its literal
  meaning only. "A bakes its logic into B" is wrong. "The oven bakes the bread"
  is literal. Say the plain fact: "A stores the value at construction."
  - Often figurative in code docs: bake, ship, live, travel, guard,
    surface, swallow, bubble, wire, under the hood, out of the box, happy
    path, world, flavor, honor, respect, aware, sibling, pay, afford,
    invite, go through, pull in. `references/words.md` has the full list.
  - A word that looks figurative but has a technical meaning in the
    domain stays: catch an exception, pin a version.
- "Keep" means "don't remove". It doesn't state a requirement or a state.
  "A workaround has to have a bug link", not "a workaround keeps its bug
  link". "The list has one entry", not "the list keeps one entry".
- No filler. Delete: note that, basically, simply, just, actually,
  essentially, of course, it is worth noting. "In order to" becomes "to".
  `references/words.md` has the full list.
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

## Shape of a doc comment

- First sentence: what it is or what it does, in words the name doesn't
  already give. A function starts with its action: "Returns", "Registers",
  "Writes". A type or property starts with a noun phrase: "The timeout of
  each request." When the name gives every fact, write no comment. Never
  start with "Also".
- Then the facts from the keep test. One sentence each, or a list or a
  table when [Form](#language-rules) says so: modes, options, steps,
  conditions.
- A code example when it shows the reader how to use the declaration
  faster than words do. Keep it short. No comments inside the example. For
  more examples, link to the website.
- Tags, in this order:
  - `@param` only when the name and the type don't say it. A public
    `@param` gets one short sentence even when the doc of the type gives
    the long form, because the reader opens one declaration at a time.
  - `@return` only when the first sentence doesn't say it.
  - `@throws` when the caller can catch or check for the exception. An
    argument or configuration error that stops the program gets no tag.
- Most doc comments fit in one to three sentences.
- A one-line doc on a member of a group can be a noun phrase: "The timeout
  of `read`." A noun phrase has no verb, so the sentence rules don't apply
  to it.

## Inline comments

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
`{0}` has a key that this version of the tool doesn't know. Remove the
key, or update the tool.
```

## Examples

Before (public):

```
/**
 * Marks a declaration so that the unused-code check deliberately skips
 * it, which is useful because some declarations are only ever reached
 * through reflection (for instance by a serialization framework or a
 * dependency injection container), so the static analysis that the check
 * performs cannot see any callers and would otherwise flag them as dead
 * code, which is misleading. Note that the check still runs on everything
 * else in the file.
 */
annotation class UsedByReflection(val caller: String)
```

After:

```
/**
 * Exempts the declaration from the unused-code check.
 *
 * Use it when only reflection calls the declaration. Name the framework
 * that calls it in [caller].
 *
 * @see [Unused code](https://example.org/checks/unused-code)
 */
annotation class UsedByReflection(val caller: String)
```

Before (private):

```
// We deliberately keep the index file outside the output directory. The
// packaging step zips everything in the output directory, and an index
// inside the archive would be picked up by the loader as a plugin, which
// is obviously not what we want. The index is regenerated on every run
// anyway, so it can never go stale.
```

After:

```
// Not in the output directory: the packaging step zips that directory,
// and the loader treats each file in the archive as a plugin. Every run
// regenerates the index.
```

Before (parallel facts in a paragraph):

```
/**
 * Runs the checks. The `fast` mode runs only the syntax checks and takes
 * about a second. The `full` mode also runs the type checks and takes
 * about a minute. The `ci` mode is `full` plus the lint, and it fails on
 * a warning.
 */
fun check(mode: Mode)
```

After:

```
/**
 * Runs the checks in one of three modes:
 *
 * - `fast`: syntax checks only. About a second.
 * - `full`: syntax and type checks. About a minute.
 * - `ci`: `full` and the lint. Fails on a warning.
 */
fun check(mode: Mode)
```

Before (restates the code):

```
/** Configures the retry policy. */
fun retryPolicy(configure: RetryPolicy.() -> Unit)
```

After: no comment. When the project requires one: "Sets how many times a
failed request runs again, and the delay between the runs."

`references/examples.md` has more pairs, including inline comments,
docstrings, messages, and a README table.

## Lint

The lint is a complement to the rules, never the primary check. It finds
punctuation and the words in `references/words.md`, and nothing else.

What the lint can't see:

- A sentence that fails the keep test.
- A fact stated twice.
- A reason given to a reader who knows it.
- A figurative use of a word that isn't in the list.
- An ambiguous sentence.
- A passive with a contracted verb.
- A wrong claim about the code.
- A paragraph that has to be a list or a table.

How to use the lint:

- The items above are most of the rules. You find them only when you
  read the text as the reader.
- A text with no findings can still break most of this skill.
- Apply the rules first, then run the lint.
- Never report a clean lint as the result of the skill.

```
python3 scripts/doc_lint.py [--json] [--max-words N] FILE...
```

| Finding | Exit code | What it is |
|---|---|---|
| Hard failure | 1 | A semicolon, an em dash, an en dash, a double hyphen, or a hyphen with a space on each side. |
| Soft warning | 0 | A sentence over the limit, a filler word, a Latin abbreviation, a word with a plainer swap, a figurative word, a likely passive, an "-ing" clause, or an uncontracted negative. A question, not an order. |

The lint reads its word lists from `references/words.md`, so the two
never differ.

What the lint reads in each kind of file:

| File | Reads | Skips |
|---|---|---|
| Source | The `/* */`, `//`, and `#` comments and the triple-quoted strings. | String literals, so a message in source code in place. |
| `.json` | Every string value that has a space in it. | Identifiers, paths, and URLs. |
| `.md` | Every paragraph, heading, list item, table row, front matter value, and link text. Every finding is a soft warning, because the lint can't tell prose from markup it doesn't know. | Code blocks, HTML tags, HTML comments, images, template calls, and link reference definitions. |

The lint can't lint one message, one string, or a text in another doc
format. Put the text in a temporary `.md` file and lint that file.

## Final check

- Every sentence passed the keep test.
- No public doc names a private type, a module, a build tool, or an
  internal mechanism.
- Public docs state defaults and tell when to use the declaration.
- Each term has one name in the file.
- No fact appears twice in the file.
- No idiom, no filler, no Latin abbreviation, no semicolon, no dash aside.
- Three or more parallel facts are a list or a table, not a paragraph.
- In a rewrite task, the code didn't change. Diff the file and look at
  the non-comment lines.
- The lint reports no hard failure, and each soft warning has an answer.
  A clean lint doesn't show that the items above hold. Reading does.
