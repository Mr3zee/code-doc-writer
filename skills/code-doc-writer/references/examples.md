# Examples

Each pair shows a text that breaks the rules and the text that passes
them. Most examples use Kotlin syntax. One is a Python docstring. The rules
are the same for every language and comment syntax.

## Public doc that explains the implementation

Before:

```
/**
 * Rewrites every source file so that each deprecated call site is
 * replaced with the replacement that the deprecation message suggests.
 *
 * The command exists for migrating a large codebase: fixing hundreds of
 * call sites by hand is error-prone, and the replacement is mechanical, so
 * a tool does it in one pass while the reviewers focus on the few sites
 * that the tool can't handle.
 *
 * Internally, the command runs the compiler once per module, collects the
 * deprecation diagnostics from each run, and hands the whole list to one
 * fixer process. It never edits a file while a compiler is running.
 */
```

After:

```
/**
 * Replaces each deprecated call with the replacement from the deprecation
 * message. Use it to migrate a codebase in one pass.
 */
```

Why: the second paragraph is a design argument. The third describes
internal mechanics. The reader of a public command doc needs the effect
and when to run it.

## Public doc with dash asides

Before:

```
/**
 * Returns the user's display name - or the login, if the display name is
 * empty - but never null, since callers use it directly in UI labels.
 */
fun displayName(): String
```

After:

```
/**
 * Returns the display name, or the login when the display name is empty.
 */
fun displayName(): String
```

Why: the return type says "never null". What the callers do with the
value isn't a fact about this function.

## Property doc that argues

Before:

```
/**
 * Whether to warn when a request has no timeout. A request without a
 * timeout can block a worker thread forever if the server never answers,
 * which in practice happens often enough that we decided the plugin
 * should nudge users toward setting one. `true` by default, set to
 * `false` to silence the warning.
 */
val warnOnMissingTimeout: Property<Boolean> = property().convention(true)
```

After:

```
/**
 * Whether the build warns on a request without a timeout.
 *
 * Default is `true`.
 */
val warnOnMissingTimeout: Property<Boolean> = property().convention(true)
```

Why: the code shows the default, but a public reader doesn't read the
code. The default is a public contract, so the doc states it. The
rationale for the warning doesn't belong here.

## Private doc that repeats the code

Before:

```
/**
 * Maps between a file's original text and its normalized form. The
 * parser only reads normalized text, and the compiler records offsets
 * against the original bytes, so the caller resolves targets on
 * [normalizedText] and then maps each insertion offset back with
 * [toRawOffset], applying the insertions to the untouched original. That
 * way the edit never rewrites existing line endings, whichever mix of
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

## Inline comment that repeats the code

Before:

```
// Retry the request up to three times with a short delay between the
// attempts, since the server sometimes returns 503 right after a deploy.
repeat(3) {
    val response = client.send(request)
    if (response.status != 503) return response
    delay(500)
}
```

After:

```
// The server returns 503 for a few seconds after a deploy.
repeat(3) {
    val response = client.send(request)
    if (response.status != 503) return response
    delay(500)
}
```

Why: the count and the delay are in the code. The behavior of the server
isn't.

## Why the code doesn't do the obvious thing

Before:

```
// We compare the fields one by one here rather than using the generated
// equals(), since the generated equals() also looks at the timestamp
// field, and two events that differ only in their timestamp should be
// treated as the same event for the purpose of deduplication.
```

After:

```
// Not `equals()`: it compares `timestamp`, and deduplication ignores it.
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
// Library version 2.4+ activates the feature the moment the `metrics`
// property is touched (its getter has that side effect, so it must not
// be called here). Activation is observed through the listeners it
// registers instead.
```

After:

```
// The getter of `metrics` activates the feature in library version 2.4
// and later, so don't read it. The registered listeners show the
// activation instead.
```

Why: this is an external constraint with a version, so it stays. It is
an instruction to the next editor, so the reason comes first and then the
instruction.

## Workaround

Before:

```
// Flush twice. For some reason one flush isn't enough on Windows.
```

After:

```
// One flush loses the last block on Windows: https://example.org/bugs/4521
```

Why: a workaround has to have a bug link. The link tells the next editor
when the workaround can go.

## Repeated boilerplate across declarations

Before, on 20 option classes:

```
 * See the [documentation](https://example.org/options/x) for the full
 * rationale and examples.
 *
 * @param name the name under which the option is registered in the
 *   registry, which must be unique within the plugin.
 * @param description a free-form human readable description. It may be
 *   left empty only if the name is self-explanatory on its own.
```

After, on each:

```
 * @param name the registry key. Unique in the plugin.
 * @param description the help text. Empty only when [name] explains the
 *   option.
 * @see [Option x](https://example.org/options/x)
```

Why: a public reader opens one class and doesn't see the others, so each
class gets the `@param` text. One short sentence for each. The full rule
is on the shared base class.

## Paragraph that holds a list

Before:

```
/**
 * Loads the configuration. The loader reads the file that `path` names,
 * then the `APP_CONFIG` environment variable, then the defaults, and the
 * first source that has a key wins. A missing file is an error, but a
 * missing variable isn't.
 */
fun loadConfig(path: Path): Config
```

After:

```
/**
 * Loads the configuration from the first source that has each key:
 *
 * 1. The file at [path]. A missing file is an error.
 * 2. The `APP_CONFIG` environment variable. A missing variable isn't an
 *    error.
 * 3. The defaults.
 */
fun loadConfig(path: Path): Config
```

Why: three sources in an order. A numbered list shows the order, and each
item holds the one fact about its source.

## README paragraph that holds a table

Before:

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

Why: three items with the same two attributes. The reader finds one
option, or compares the defaults, and skips the rest.

## Message

Before:

```
`@RequiresPermission` on `{0}` does not list any permission, so any caller
can invoke it without holding anything, and the check that the annotation
was meant to provide is effectively lost. Please list at least one
permission, with a short explanation of why access is restricted.
```

After:

```
`@RequiresPermission` on `{0}` lists no permission, so any caller can call
it. List at least one permission.
```

Why: problem, then fix. The reason for the permission belongs on the
check's page, not in the message.

## Log line

Before:

```
log.info("Successfully finished processing all of the $count report files that were collected from the compilations, now handing them off to the fixer")
```

After:

```
log.info("Collected $count reports.")
```
