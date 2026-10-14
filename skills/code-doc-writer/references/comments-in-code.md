# Comments in code

Decide the reader first. [Two readers](../SKILL.md#two-readers) lists which
declarations have user docs.

- When the name or the code gives every fact, write no comment.
  For a private declaration this is by far the most common outcome.
- First sentence: what it is or what it does, in words the name doesn't
  already give. A function starts with its action: "Returns", "Registers",
  "Writes". A type or property starts with a noun phrase: "The timeout of
  each request." Never start with "Also".
- Then the facts from the keep test. One sentence each, or a list or a
  table when [Form](../SKILL.md#language-rules) requires one.
- A code example when it shows the reader how to use the declaration
  faster than words do. The example is short and has no comments inside
  it. For more examples, link to the website.
- Tags, in this order:
  - `@param` only when the name and the type don't give it. A `@param` in
    user docs gets one short sentence even when the doc of the type gives
    the long form, because the reader opens one declaration at a time.
  - `@return` only when the first sentence doesn't give it.
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
- Delete a comment that repeats what the next lines do. The code shows it.
  This includes a comment that names the algorithm: "binary search",
  "lower bound", "iterate over the handlers".
- Put the comment where the decision is.
- Three or more parallel facts, such as the cases of a branch, go in a
  list with one item on each line.
