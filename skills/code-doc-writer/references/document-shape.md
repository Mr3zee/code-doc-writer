# Shape of a document

- Follow the shape of the existing pages of the same kind.
- One topic in each section. The headings alone give the outline.
- The common case comes before the exceptions. A rule comes before the
  example that shows it.
- A changelog entry states what changed for the reader, not what changed in
  the code.

# Shape of a pull request description

The reader is a reviewer. They have the diff, the commit list, and the
linked issue. The description holds what the diff can't show.

- The title is one sentence that states what changed for the user or the
  developer, not which files changed. "Retry a failed upload three
  times", not "Update UploadService".
- The body has these parts, in this order. Omit a part that has no
  facts.
  1. The reason for the change, when the linked issue doesn't give it.
     In a pull request the reason is a fact the reviewer needs, so the
     keep test keeps it.
  2. What changed in behavior. One list item for each change that the
     diff doesn't show in one place: a changed default, a removed path,
     a new limit.
  3. What the reviewer must check or run. A risk, a part that has no
     test, a migration step.
  4. The link to the issue, in the form that the project uses.
- No list of commits or files. The reviewer has both.
- No history of the branch: "first I tried", "after review I moved".

# Shape of an issue description

The reader is a developer who will fix the bug or build the feature.
They have the code. They don't have the reporter's environment, input,
or goal. The description holds what they can't get from the code.

- The title is one sentence that names the wrong behavior or the missing
  behavior. "`parse` returns an empty list for a file with a BOM", not
  "Parser bug".
- A bug report has these parts, in this order:
  1. The steps that cause the bug. A command, an input, or a code
     sample that the developer can run. The smallest one that still
     shows the bug.
  2. What happens. The exact output or error text, in a code block.
  3. What must happen instead.
  4. The versions and the platform, when the bug can depend on them.
  5. A link to a related issue, a log, or a project, when one exists.
- A feature request has these parts, in this order:
  1. The task that the reader can't do, or can do only with a
     workaround. Give the workaround.
  2. The behavior that would do it. When more than one design fits,
     name the task and stop.
- No guess at the cause unless the reporter checked it in the code. A
  checked cause goes after the expected behavior, with the file or the
  function.
- No history of how the reporter found the bug and no sentence about its
  importance. The reader decides the priority from the facts.
