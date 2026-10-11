# Examples

Each pair shows a comment before and after the rewrite. Most examples use
Kotlin syntax. One is a Python docstring. The rules are the same for every
language and comment syntax.

## Public doc that explains the implementation

Before:

```
/**
 * Rewrites the module's sources so that every recorded diagnostic is
 * acknowledged with the matching exemption annotation.
 *
 * The task is meant for adopting the checks on an existing library: the
 * already-shipped API can't change shape without breaking users, so its
 * diagnostics are acknowledged wholesale and the checks keep guarding
 * only the API added afterwards.
 *
 * When this task is selected, every main compilation writes a report
 * through the regular compile task. This task depends on those
 * compilations, hands all reports to one standalone fixer process, and
 * never invokes a compiler itself.
 */
```

After:

```
/**
 * Adds an exemption annotation to every declaration with a recorded
 * diagnostic. Use it when you adopt the checks on a published library.
 */
```

Why: the second paragraph is a design argument. The third describes
internal mechanics. The reader of a public task doc needs the effect and
when to run it.

## Public doc with a long aside

Before:

```
/**
 * Acknowledges that the annotated DSL marker deliberately keeps wrong
 * target set - no-op targets in its `@Target`, or no explicit `@Target`
 * at all - because fixing it would break existing users.
 */
```

After:

```
/**
 * Exempts a published DSL marker whose `@Target` is wrong (no-op targets,
 * or no `@Target`) and can't change.
 */
```

## Property doc that argues

Before:

```
/**
 * Whether to suggest enabling binary compatibility validation when
 * neither plugin is active. The check reviews the shape of new API
 * declarations, while binary compatibility validation guards the API
 * that already shipped, so the plugin recommends it with a build
 * warning. `true` by default, set to `false` to silence the suggestion.
 */
val suggestAbiValidation: Property<Boolean> = property().convention(true)
```

After:

```
/**
 * Whether the build warns when no binary compatibility validation plugin
 * is active.
 *
 * Default is `true`.
 */
val suggestAbiValidation: Property<Boolean> = property().convention(true)
```

Why: the code shows the default, but a public reader doesn't read the
code. The default is a public contract, so the doc keeps it. The rationale
for the warning doesn't belong here.

## Private doc that repeats the code

Before:

```
/**
 * Maps between a file's original text and its normalized form. The
 * parser only reads normalized text, and the compiler records offsets
 * against the original bytes, so the fixer resolves targets on
 * [normalizedText] and then maps each insertion offset back with
 * [toRawOffset], applying the insertions to the untouched original. That
 * way the fix never rewrites existing line endings, whichever mix of
 * `\r\n`, `\n`, and stray `\r` the file carries. Only the inserted text
 * itself uses [newline], the file's dominant separator.
 */
class LineEndingMapping
```

After:

```
/**
 * Maps offsets in the `\n`-normalized text back to the original text.
 * The parser needs normalized text. The compiler reports offsets in the
 * original bytes.
 */
class LineEndingMapping
```

Why: the method names say what they do. The two facts that the code can't
show are the two constraints from outside.

## Inline comment that repeats what the code shows

Before:

```
// Comparisons instead of a `when` over the enum: an exhaustive `when`
// compiles to an `ordinal()` switch, and the compatibility checker
// rejects that call against the compiler API baseline.
```

After:

```
// Not a `when`: it compiles to an `ordinal()` call that the compatibility
// checker rejects against the compiler API baseline.
```

## Inline comment that narrates the code

Before:

```
// Iterate over all checkers and register each one with the session.
for (checker in checkers) session.register(checker)
```

After: no comment.

## Docstring

Before:

```
def resolve(self, name):
    """
    Attempts to resolve the given name by looking it up in the local
    scope first and then, if it is not found there, falling back to the
    parent scope (if any), which allows nested scopes to shadow outer
    bindings in the usual way.
    """
```

After:

```
def resolve(self, name):
    """Returns the binding for `name` from this scope or the nearest parent
    scope that has it. Returns `None` when no scope has it."""
```

## Constraint that must stay

Before:

```
// Kotlin 2.4+ activates ABI validation the moment the `abiValidation`
// DSL property is touched (its getter has that side effect, so it must
// not be called here). Activation is observed through the tasks it
// registers instead.
```

After:

```
// The getter of `abiValidation` activates ABI validation in Kotlin 2.4
// and later, so don't read it. The registered tasks show the activation
// instead.
```

Why: this is an external constraint with a version, so it stays. It is
an instruction to the next editor, so the reason comes first and then the
instruction.

## Repeated boilerplate across declarations

Before, on 20 annotations:

```
 * See the [documentation](https://example.org/checks/x) for the full
 * rationale and examples.
 *
 * @param reason why the declaration deliberately exposes this shape.
 * @param description free-form explanation of the exemption. May be
 *   empty only when [reason] explains the exemption on its own.
```

After, on each:

```
 * @param reason why the shape stays.
 * @param description the constraint. Empty only when [reason] gives the
 *   whole constraint.
 * @see [Check x](https://example.org/checks/x)
```

The `@param` text stays on each annotation, because a public reader reads
any one of them. It gets one short sentence each. The long version of the
rule is on the shared `reason` enum.

## Message

Before:

```
`@SubclassOptInRequired` lists no marker classes, so any external class can
subclass `{0}` without opting in to anything, and the library keeps the
evolution risk it meant to opt out of. Pass at least one opt-in marker
class with a description of why the subclassing is restricted.
```

After:

```
`@SubclassOptInRequired` on `{0}` lists no marker class, so any external
class can subclass it. Pass at least one opt-in marker class.
```

Why: problem, then fix. The reason for the marker belongs on the check's
page, not in the message.

## Log line

Before:

```
log.info("Successfully finished processing all of the $count report files that were collected from the compilations, now handing them off to the fixer")
```

After:

```
log.info("Collected $count reports.")
```
