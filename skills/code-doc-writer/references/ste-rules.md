# STE rules for technical docs

ASD-STE100 Issue 9 (2025) has 9 sections of writing rules and a dictionary.
This file gives each rule in short form and says how it applies to
documentation, messages, and code comments. Read it when a rule in
SKILL.md needs its source.

## Section 1: Words

- 1.1 Use approved words, technical nouns, and technical verbs. In
  technical docs the technical nouns are identifiers, tool names, formats,
  and domain terms. The technical verbs are the domain's own verbs. `words.md` has
  the table.
- 1.2 Use a word only as its approved part of speech. "Test" is a noun.
  "Do a test", not "test the system". In code, use the domain's term: "run
  the tests".
- 1.3 Use a word only with its approved meaning. This is the rule against
  idioms and metaphors. "Follow" means "come after". It doesn't mean
  "obey".
- 1.4 Use only the approved forms of verbs and adjectives.
- 1.5 Technical nouns: a word is a technical noun when it belongs to a
  subject field. STE lists 22 categories. Category 19 is computer science.
- 1.6 Use an unapproved word only when it is a technical noun. STE rejects
  "backup" as a word but accepts it as a computer term.
- 1.7 Don't use a technical noun as a verb. "Apply oil", not "oil the
  part". In code, "cache the result" is an accepted technical verb.
- 1.8 Use the technical nouns of your field. Use the name the code uses.
- 1.9 When you pick a technical noun, pick a short one.
- 1.10 No regional, slang, or jargon words. "Brick the router" is slang.
  "Footgun", "gotcha", "magic" are slang.
- 1.11 One technical noun for one item. Never two names for one thing.
- 1.12 Technical verbs: category 2 is computer processes. Enable, disable,
  install, load, update, debug, boot, format, and more. STE rejects
  "enable" and "disable". This skill accepts them for a feature ("enable
  the cache"), not for a person ("enable the user to"). See
  `words.md`.
- 1.13 Don't use a technical verb as a noun. In code, "cache" and
  "override" are both a verb and a noun, each with one meaning.
- 1.14 American spelling.

## Section 2: Multi-word nouns

- 2.1 At most three words in a noun group. "Runway light connection
  resistance calibration" becomes "calibration of the resistance of the
  runway light connection". In code: "the request timeout option", not
  "the HTTP client request timeout command line option".
- 2.2 Write a long technical noun in full the first time. Then use its
  short form or abbreviation. Hyphens join words that are one unit.

## Section 3: Verbs

- 3.1 Use the verb forms in the dictionary.
- 3.2 Allowed forms: infinitive, imperative, simple present, simple past,
  simple future, past participle as an adjective. Not allowed: perfect
  tenses ("has returned"), progressive ("is returning").
- 3.3 The past participle is an adjective. "The sorted list."
- 3.4 No auxiliary verbs for complex constructions. "The value can be
  changed" becomes "You can change the value".
- 3.5 "-ing" only in a technical noun or as its modifier. "Caching",
  "logging", "the parsing step" are fine. "When parsing" isn't.
- 3.6 Active voice. In descriptions the passive is allowed only when the
  actor is unknown. Four methods to fix a passive: name the actor, change
  the verb, use the imperative, use "you" or "we".
- 3.7 Use a verb for an action, not a noun. "The method shows", not "the
  method gives an indication".

## Section 4: Sentences

- 4.1 Short and clear. One topic in each descriptive sentence. Not
  abstract: "No leaks are permitted" becomes "Make sure that there are no
  leaks".
- 4.2 Don't omit words to make a sentence shorter. Keep the subject, the
  verb, the articles, and "that". Write words in full, except the
  negative contractions that `words.md` lists.
- 4.3 Use a vertical list or a table for three or more parallel facts.
  Colon at the end of the lead sentence. Each item starts with an
  uppercase letter or with a label in a code span. Each item ends with a
  period, a noun phrase too. The Form rules in SKILL.md give the details.
- 4.4 Connecting words join related sentences: and, but, then, thus, as a
  result.
- 4.5 Use an article or "this" before a noun when English needs one. No
  article before a general concept or before a name with an identifier.

## Section 5: Procedural writing

Instructions. In technical docs: a step in a procedure, a fix in a
message, and a "how to use" sentence. Also `@param` text that tells the
caller what to do.

- 5.1 At most 20 words in a sentence.
- 5.2 One instruction in a sentence, unless two actions happen together.
- 5.3 Imperative form. "Close the stream."
- 5.4 Condition first, then the instruction, with a comma. "If the file is
  open, close it."
- 5.5 A note gives information only, never an instruction or a limit.

## Section 6: Descriptive writing

Descriptions. In technical docs: what a feature, a page, or a declaration
is or does.

- 6.1 Give information step by step. One subject in each sentence.
- 6.2 Repeat key words to connect sentences. Don't vary the term.
- 6.3 At most 25 words in a sentence.
- 6.4 A paragraph starts with a topic sentence.
- 6.5 One topic in a paragraph.
- 6.6 At most six sentences in a paragraph. A paragraph is for one fact
  or for a line of argument. A line of argument can also be a list, with
  one step in each item.

## Section 7: Safety instructions

One rule applies to technical docs: a warning about a harmful call starts
with the command, then gives the risk. "Don't call this from the UI
thread. It blocks until the file is read." Every other instruction puts
the condition or the reason first (rule 5.4).

## Section 8: Punctuation and word count

- 8.1 All standard punctuation, but no semicolon.
- 8.2 Hyphens join directly related words: "read-only", "thread-safe".
- 8.3 Parentheses only for a reference, an identifier, an abbreviation, a
  singular and plural at once, a short explanation, or an alternative.
- 8.4 to 8.7 Word count: a parenthesis, a number with its unit, an
  abbreviation, an identifier, quoted text, a title, and a hyphenated word
  each count as one word. A colon before a list ends the sentence.

## Section 9: Writing practices

- 9.1 When a word-for-word swap doesn't work, write a new sentence.
- 9.2 Use each approved word correctly. "See" is for eyes and for a
  reference to a document. "Make sure" is for a check.
- 9.3 No phrasal verbs. "Extinguish", not "put out". In code: "start", not
  "kick off". "Remove", not "strip out". "Send", not "hand off".
- 9.4 Consistent style. The same wording for the same kind of fact,
  everywhere.
- GR-1 Keep "that" after "make sure", "show", "recommend".
- GR-2 "With" can be ambiguous. Write the condition first.
- GR-3 A pronoun must have one clear referent. Repeat the noun if not.
- GR-4 "This" must point to one thing.
- GR-6 No Latin abbreviations.
- GR-7 Gender-neutral language.
- GR-8 Use the possessive form only when no other reading exists.
