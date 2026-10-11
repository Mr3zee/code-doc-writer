# Words

The STE dictionary approves about 900 words and rejects about 1300 with
alternatives. This file is the part that matters for code docs, adapted
for programming. The adaptation: exact terms of computer science stay, even
when STE rejects them. STE itself has this exception in its technical noun
and technical verb categories (rules 1.5 and 1.12, category "computer
processes").

`scripts/doc_lint.py` reads its word lists from this file: the two swap
tables, the delete list, and the figurative list. A change here changes
the lint. Keep the format of each list: one table row or one bullet, items
separated by commas, a condition in parentheses after the item.

## Plain verbs to prefer

| Use | Instead of |
|---|---|
| do | perform, carry out, conduct |
| get, fetch | obtain, retrieve, acquire, receive (a value) |
| give | provide, supply, furnish, offer |
| make | create (an object), construct, build (an object), produce |
| use | utilize, utilise, employ, leverage, make use of |
| set | assign, specify (a value) |
| show | indicate, display, represent, denote, signify, reflect |
| find | determine, locate, discover, look up, detect |
| let | allow, permit |
| need | require (when it means need) |
| keep (only for "don't remove") | retain, preserve, maintain, hold on to |
| put | place, insert, position |
| start | begin, commence, initiate, launch |
| stop, terminate | terminate, cease, halt |
| send | transmit |
| read, write | save (a file), persist |
| check, make sure | verify, ensure, guarantee, make certain |
| add, remove | append (unless order matters), drop, strip |
| change | modify, alter, adjust, update |
| call | invoke |
| run | execute (a program or task) |
| fail | error out, blow up |
| cause | trigger (when it means cause), result in, lead to |
| help | facilitate, assist, aid |
| have | comprise, consist of, contain (when it means have) |
| be | constitute |
| think, expect | assume, consider |
| tell | inform, notify |

All words in the instead of have an exception: 
`Unless the term is '<this word>'.`

## Computer science terms that stay

These are technical verbs and nouns. They are exact. A plain verb loses
meaning. Use each with its one meaning.

- Verbs: compile, parse, resolve, register, configure (an object, not a
  value), enable and disable (a feature, not a permission), install, load
  (into memory), publish, deploy, serialize, deserialize, encode, decode,
  encrypt, cache, index, sort, filter, map, reduce, merge, split, validate
  (against a schema), handle (an event or exception), throw (an exception
  that the caller catches), catch, return, yield, await, lock, unlock,
  commit, roll back, fetch (git), push, pull, clone, mount, bind, override,
  inherit, implement, instantiate, allocate, free, dispose, close, mutate,
  open, flush, poll, subscribe, emit (an event), dispatch (an event),
  report (a diagnostic), suppress (a diagnostic), inline, link, relocate,
  shade, delete, include, fall back (to a default).
- Whether: before a Boolean property or function. "Whether the check
  runs."
- Nouns: API, build, cache, callback, classpath, compilation, dependency,
  default, diagnostic, exception, fallback, handler, hook, invariant,
  listener, module, option, override, parser, plugin, property, provider,
  registry, runtime, scope, session, severity, target, task, token, type,
  variant, visibility, warning, error.

"Keep" means "don't remove". For a requirement, write "has to have" or
"must have". For a state, write "has". Not "the task keeps its output",
but "the task has to have an output" or "the task has an output".
Use "default" as a noun or adjective. The verb form "defaults to X" is an
accepted term.
"Fallback" is the noun, "fall back to" is the verb. "The loader falls back
to the bundled file."

## Words to delete

Filler adds no fact. Delete it and read the sentence again.

- note that, please note, it is worth noting, it should be noted, notably,
  importantly, interestingly, unfortunately
- basically, simply, just, actually, essentially, effectively, really
- very, quite, rather, fairly, somewhat
- obviously, of course, clearly, naturally, needless to say
- deliberately, on purpose, intentionally, by design, honest, honestly,
  meant to
- in other words, that is to say, in this way, at this point, in terms of
- currently, at the moment, for now (version control has the time)
- keep in mind, bear in mind, make sure to (write the instruction)
- respective, respectively, desired, aforementioned, as follows
- etc., viz.

## Words with a plainer swap

| Replace | With |
|---|---|
| however, nevertheless, nonetheless | but |
| therefore, hence, consequently | thus, so |
| additionally, furthermore, moreover | also |
| subsequently, afterwards | then |
| whilst | while |
| amongst | among |
| approximately | about |
| via | through, with |
| within | in |
| upon | on, when |
| prior to | before |
| subsequent to | after |
| as well as, in addition to, along with | and |
| due to the fact that, owing to, since (causal) | because |
| in the event that, in case | if |
| in the case of | for |
| regarding, with regard to, with respect to | about |
| a number of | some |
| various, a variety of | different |
| numerous, multiple | many, several |
| is able to, is capable of, has the ability to, it is possible to | can |
| may, might, could, would | can |
| should, ought to | must, or delete |
| appropriate | applicable, correct |
| relevant, corresponding | related, matching |
| particular, specific, certain | delete, or "some", "one" |
| the following | these, this |
| which is why, which means that | thus, so |
| so that (purpose) | to |
| in such a way that | so |
| to the extent that | if |
| in order to, so as to | to |
| whenever | when |
| once (time) | after, when |
| per | for each |
| meant for | for |
| there is, there are | name the actor |
| e.g. | for example |
| i.e. | that is |
| cf. | compare |
| vs. | or |
| a.k.a., aka | also |

## Often figurative

These words are figurative in most code docs. Literal use is fine: "the
oven bakes the bread". The lint flags each form of the word (bakes, baked,
baking) and asks.

- bake, ship, live, land, travel, walk, sit, sit on top, bridge, bleed,
  leak, poison, pollute, hijack, steal, sweep, funnel, gate, guard, wire,
  plumb, plumbing, glue, surface, bubble, swallow, fire
- spell out, stand in, stand-in, pick up, kick in, kick off, hand off,
  wrap up, roll up, boil down, go through, pull in, come into play, take
  care of
- under the hood, out of the box, happy path, hot path, escape hatch,
  heavy lifting, through the lens, at the end of the day, in a nutshell,
  on the fly, first class, first-class, citizen, umbrella
- world, flavor, blessed, sane, sanity, magic, footgun, gotcha, trick,
  hack, lightweight, stale, fresh, sibling, cousin
- honor, honour, respect, aware, friendly, smart, dumb, naive, clever,
  promote, demote, pay, paid, afford, invite

## Contractions

STE writes every word in full. This skill differs: use the common negative
contractions can't, don't, doesn't, isn't, won't, didn't, aren't, wasn't.
Never "cannot". Don't use other contractions (it's, you're, we've).

## Modal verbs

- "can" for possibility and permission.
- "must" for a requirement on the reader.
- "will" only for a real future event. Behavior is in the present tense.
- "may", "might", "could", "should", "would" don't appear.
