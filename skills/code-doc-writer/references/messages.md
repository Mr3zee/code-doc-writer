# Messages

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

