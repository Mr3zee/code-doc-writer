---
name: code-doc-writer
description: >-
  Write or rewrite every text a person reads in code or in documentation,
  in short plain technical English based on ASD-STE100: doc comments
  (KDoc, Javadoc, JSDoc, Doxygen, docstrings, XML docs, rustdoc, Go doc
  comments), inline comments, TODO and FIXME notes, user-facing messages
  (diagnostics, errors, exceptions, assertions, warnings, deprecation
  notices, log lines, CLI output, help text, message templates), and
  any documentation: README files, changelogs, docs websites, guides,
  Markdown, reStructuredText, AsciiDoc, or any other doc format. Use it
  every time you write, change, or delete such a text, in any language,
  during any task, even a one-line comment that is a side effect of a
  code change. Also use it when someone asks to cut the bullshit,
  simplify, shorten, clean up, remove the noise from, or review docs,
  comments, or messages, or asks for STE or Simplified Technical English.
---

# Code doc writer

Write comments, messages, and documentation so a reader gets the facts
fast. The language rules come from ASD-STE100 (Simplified Technical
English), adapted for programming. The scope rules come from one idea: a
comment is only for what the code can't say. Each sentence costs the
reader time and the next editor upkeep, so the text that gives the facts
in the fewest sentences wins. No comment is a good result when the code
gives every fact.

## Scope

- Every doc comment, inline comment, and user-facing message that you write
  or change, during any task. A rewrite follows the same rules as a new
  text.
- User-facing messages are diagnostics, errors, warnings, log lines, CLI
  output, and message templates in data files. A task that names only the
  comments of a file still covers the messages in that file. "Don't
  change the code" means the logic. A message string is text, not logic.
- Comments in data files are private docs: a `$comment` key in JSON, a `#`
  line in YAML, a comment block in a template.
- Any documentation: README files, changelogs, docs websites, guides,
  Markdown, reStructuredText, AsciiDoc, or any other doc format. The
  language rules apply as they are. The scope rules apply with the doc
  as the reader's one place: a doc states every fact the reader needs
  there.
- The skill applies to the text, not the code. When you write code, the
  skill applies to the comments and messages you write with it. Keep the
  comment syntax of the language. When the task is a rewrite, change text
  only: no code, imports, annotations, placeholders, or code formatting.
- A generated file gets its text from a template. Edit the template.
- Keep the syntax of links, references, and tags that a tool reads, such
  as `@see`, `[Name]`, `{@link}`, `{0}`. The keep test decides whether a
  `@param` or a `@throws` is there.

## Two readers

| | Public API docs | Private docs |
|---|---|---|
| Reader | A user of the library. Smart, but doesn't read the source. | A developer of this codebase. Knows the domain and the modules. |
| Tell | What it does. When to use it. How to call it. What the caller must know. | Only what the code can't show. |
| Never | Implementation, internal types, other modules, build tooling, history, design arguments. | What the code already shows. What the public docs already say. History. |

A declaration is public API when a user of the published artifact can see
it. Visibility alone doesn't decide. A public class in a module that users
never depend on has private docs. Check the module's purpose before you
decide.

A public reader learns from one place: the website, the README, the doc
comment in the IDE, or one overload of a function. Each place carries the
facts the reader needs there. A public doc can repeat a fact that the
website, the README, or another overload also gives. Never send a public
reader elsewhere for a fact the caller must know. Use `@see` for related
API, not for required facts.

A public doc also states a lazy or cached computation and a side effect.
The reader doesn't open the source.

A private reader has the source and the public docs. A private doc repeats
a public fact only to add to it.

## Procedure

1. Read `DOCS_GUIDELINE.md` in the repository root if it exists. It holds
   the project's terms, link formats, required tags, and exceptions. The
   rules in that file win over this skill.
2. Read the code first. If the purpose isn't clear, read the signature,
   the body, and the callers.
3. Draft the text: one sentence for each fact that the reader needs. In a
   rewrite, the draft is the existing text, split into sentences.
4. Apply the keep test to each sentence. Delete or keep.
5. Write each kept sentence with the language rules.
6. Put the sentences in this order: what it is, what the reader must know,
   tags.
7. Check each claim about the code against the code or the project's
   docs. Fix a wrong claim. Find the fact behind an ambiguous sentence and
   write it. When you can't check a claim that comes from the original
   text, keep its wording.
8. Run `scripts/doc_lint.py` on the file. When the text isn't in a form
   the lint reads, put it in a temporary `.md` file and lint that file.
   Fix every hard failure. Read each soft warning and fix it or leave it
   with a reason.
9. In a rewrite, compare the result with the original. The result has
   every kept fact and invents none. A qualifier such as "some", "only",
   or "when X" is a fact.
10. Read the result as the reader. A sentence that doesn't change what the
    reader does or knows goes. Readability is the measure, and a shorter
    text with the same facts reads faster. A rewrite that passed the keep
    test is shorter in most files. When the result is close to the
    original in length, do the keep test again.
11. After each self-contained part (a file, a class, a group of related
    declarations), read the result once more for leftovers:
    - A sentence that referred to a deleted sentence.
    - A link to a deleted section.
    - A term that the rest of the file no longer uses.
    - A fact that now appears twice.
    - A comment that no longer matches the code below it.

The style of the request doesn't change the style of the text. A casual
or blunt request still gets a plain technical comment. When you report
your work to the person, use the same language rules.

## Keep test

Delete a sentence when one of these is true:

- The name, type, signature, or modifier already says it. One exception:
  a public doc states the default value, because the reader doesn't open
  the source.
- In private docs: another comment or the public doc already says it. Keep
  it in one place. Link to that place with a reference.
- It explains a reason to a reader who already knows the domain.
- It teaches the host language, tool, or platform instead of this
  declaration. How to declare a dependency, what `this` is in a block, how
  a language feature works.
- It tells history, intent, or feelings and nothing else. Delete the
  intent word first ("deliberately", "on purpose", "honest", "intended",
  "we chose"). Then apply the keep test to the fact that remains.
- It describes what other parts of the system do with this declaration.
  For public docs this is always a delete. For private docs, keep it only
  when a search for the name doesn't find the other part.
- It gives a second example of the same thing.

Keep a sentence when one of these is true:

- A caller can misuse the declaration without it: a precondition, a side
  effect, thread safety, ownership, order of calls, or a unit.
- It tells a public reader when to use the declaration. This rule wins
  over every delete rule. When the original gives no real condition, take
  one from the project's docs or keep the original. Never infer a
  condition from the rationale, and never delete the sentence.
- It gives a constraint from outside the code: a tool bug, a protocol, a
  version limit, a file format. Without the sentence, the next editor
  breaks it. Give the source of the constraint. A workaround has to have
  a bug link.
- It gives the one invariant that the code relies on and doesn't check.
- It tells why the code doesn't do the obvious thing.

When a delete rule and a keep rule both match a sentence, the keep rule
wins.

Add a fact that the draft lacks only when the code proves it and a caller
needs it: what happens on misuse, the error or diagnostic that the code
reports, the exception it throws.

State a default that is the same for a group of declarations once, on the
group or the class, not on each member.

When nothing is left, delete the whole comment. When the project requires
a doc comment on every public declaration, keep one sentence. That sentence
must still help: it says what the declaration is for, not its name again.

## Language rules

`references/ste-rules.md` gives the ASD-STE100 source of the rules that
come from the standard.

Sentences:

- Aim for at most 20 words in an instruction and 25 in a description. A
  code span, a link, a number, a placeholder, or a parenthesis counts as one
  word. When a split makes the sentence harder to read, or drops a fact,
  keep the long sentence.
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
- Three or more items with structure go in a vertical list.
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
  - A word with a technical meaning in the domain stays: catch an
    exception, pin a version, fall back to a default.
- "Keep" means "don't remove". It doesn't state a requirement or a state.
  "A workaround has to have a bug link", not "a workaround keeps its bug
  link". "The list has one entry", not "the list keeps one entry".
- No filler. Delete: note that, basically, simply, just, actually,
  essentially, of course, it is worth noting, deliberately, on purpose,
  honest, by design. "In order to" becomes "to".
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
- Then the facts from the keep test, one sentence each.
- A code example when it shows the reader how to use the declaration
  faster than words do. Keep it short. No comments inside the example. For
  more examples, link to the website.
- `@param` only when the name and the type don't say it. On a public
  declaration a `@param` gets one short sentence even when the doc of the
  type gives the long form, because the reader reads one declaration at a
  time. `@return` only when the first sentence doesn't say it. `@throws`
  when the caller can catch or check for the exception. An argument or
  configuration error that stops the program gets no tag.
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
- Delete a comment that says what the next lines do. The code says it.
  This includes a comment that names the algorithm: "binary search",
  "lower bound", "iterate over the handlers".
- The keep test applies.
- A workaround has to have a bug link. When the comment has none, add it.
- Put the comment where the decision is.
- No history. "Previously", "used to", "now" belong to version control.

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
  limit of an instruction. Put the messages in a temporary `.md` file and
  run the lint on it with `--max-words 20`.
- Line length rules of the code don't apply to a file with data.
- At best three sentences for the problem and the fix. A fixed closing
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

Before (restates the code):

```
/** Configures the retry policy. */
fun retryPolicy(configure: RetryPolicy.() -> Unit)
```

After: no comment. When the project requires one: "Sets how many times a
failed request runs again, and the delay between the runs."

`references/examples.md` has more pairs, including inline comments,
docstrings, and messages.

## Lint

```
python3 scripts/doc_lint.py [--json] [--max-words N] FILE...
```

Hard failures (exit code 1): a semicolon, an em dash, an en dash, a
double hyphen, and a hyphen with a space on each side. Soft warnings: a
sentence over the limit, a filler word, a Latin abbreviation, a word with
a plainer swap, a figurative word, a likely passive, an "-ing" clause, an
uncontracted negative. A soft warning is a question, not an order. The
lint reads its word lists from `references/words.md`, so the two never
differ.

The lint reads three kinds of file:

- A source file: the `/* */`, `//`, and `#` comments and the triple-quoted
  strings. String literals aren't read, so a message in source code isn't
  linted in place.
- A `.json` file: every string value that has a space in it, so
  identifiers, paths, and URLs pass.
- A `.md` file: every paragraph, heading, list item, and table row.
  Fenced code is skipped.

The lint can't lint one message, one string, or a text in another doc
format. Put the text in a temporary `.md` file and lint that file.

## Final check

- Every sentence passed the keep test.
- No public doc names a private type, a module, a build tool, or an
  internal mechanism.
- Public docs state defaults and tell when to use the declaration.
- Each term has one name in the file.
- No idiom, no filler, no Latin abbreviation, no semicolon, no dash aside.
- The lint reports no hard failure, and each soft warning has an answer.
- In a rewrite task, the code didn't change. Diff the file and look at
  the non-comment lines.
