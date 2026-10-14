"""Tests for scripts/doc_lint.py.

Run from the repository root:
    python3 -m unittest discover tests
"""
import importlib.util
import io
import json
import os
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "code-doc-writer" / "scripts" / "doc_lint.py"

spec = importlib.util.spec_from_file_location("doc_lint", SCRIPT)
dl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dl)


def dedent(text):
    return textwrap.dedent(text).lstrip("\n")


class TempFiles:
    """Writes files into a temporary directory and lints them."""

    def __enter__(self):
        self.dir = tempfile.TemporaryDirectory()
        return self

    def __exit__(self, *exc):
        self.dir.cleanup()

    def write(self, name, text):
        path = Path(self.dir.name) / name
        path.write_text(dedent(text), encoding="utf-8")
        return str(path)

    def lint(self, name, text, max_words=dl.MAX_WORDS):
        return dl.lint_file(self.write(name, text), max_words)


def rules(findings):
    return [f["rule"] for f in findings]


def texts(findings, rule):
    return [f["text"] for f in findings if f["rule"] == rule]


class WordTableTest(unittest.TestCase):
    def test_split_items_keeps_conditions(self):
        self.assertEqual(
            dl.split_items("append (unless order matters), drop, strip"),
            [("append", " (unless order matters)"), ("drop", ""), ("strip", "")],
        )

    def test_split_items_ignores_commas_inside_parentheses(self):
        self.assertEqual(dl.split_items("a (x, y), b"), [("a", " (x, y)"), ("b", "")])

    def test_tables_and_lists_load(self):
        swaps, figurative, speech = dl.load_words(dl.WORDS_FILE)
        self.assertEqual(swaps["perform"], "do")
        self.assertEqual(swaps["append"], "add, remove (unless order matters)")
        self.assertEqual(swaps["however"], "but")
        self.assertEqual(swaps["should"], "must, or delete")
        self.assertEqual(swaps["basically"], "delete")
        self.assertEqual(swaps["etc."], "delete")
        self.assertIn("bake", figurative)
        self.assertIn("under the hood", figurative)

    def test_a_plain_verb_is_not_its_own_swap(self):
        swaps, _, _ = dl.load_words(dl.WORDS_FILE)
        for word in ("do", "get", "keep", "stop", "send", "check", "add", "change"):
            self.assertNotIn(word, swaps, word)

    def test_common_figurative_words_are_in_words(self):
        for word in ("bake", "ship", "surface", "swallow", "under the hood", "happy path", "sibling", "pull in"):
            self.assertIn(word, dl.FIGURATIVE)

    def test_speech_and_thought_verbs_are_in_words(self):
        for word in ("tell", "told", "say", "said", "ask", "want", "know", "think", "complain", "promise"):
            self.assertIn(word, dl.SPEECH)
            self.assertNotIn(word, dl.FIGURATIVE)
        self.assertEqual(dl.SWAPS["tell"], "report, show (code or a text as the actor)")


class WordFormsTest(unittest.TestCase):
    def test_regular_verb(self):
        self.assertEqual(dl.word_forms("bake"), {"bake", "bakes", "baked", "baking"})

    def test_consonant_doubling(self):
        self.assertIn("shipped", dl.word_forms("ship"))
        self.assertIn("shipping", dl.word_forms("ship"))

    def test_y_ending(self):
        self.assertIn("carries", dl.word_forms("carry"))
        self.assertIn("carried", dl.word_forms("carry"))

    def test_no_es_plural_after_a_plain_consonant(self):
        self.assertNotIn("sites", dl.word_forms("sit"))
        self.assertIn("goes", dl.word_forms("go"))

    def test_phrase_inflects_its_first_word(self):
        self.assertIn("goes through", dl.word_forms("go through"))
        self.assertIn("pulled in", dl.word_forms("pull in"))


class ExtractCommentsTest(unittest.TestCase):
    def test_line_comments_join_into_one_block(self):
        blocks = dl.extract_comments("x = 1\n// first\n// second\ny = 2\n")
        self.assertEqual(blocks, [(2, "first\nsecond")])

    def test_block_comment_loses_leading_stars(self):
        text = "/**\n * Returns the size.\n * @param x the input\n */\nfun f()"
        blocks = dl.extract_comments(text)
        self.assertEqual(blocks[0][0], 1)
        self.assertEqual(blocks[0][1].strip(), "Returns the size.\n@param x the input")

    def test_hash_comments_and_shebang(self):
        text = "#!/usr/bin/env python3\nimport os\n# a comment\nx = 1  # trailing\n"
        blocks = dl.extract_comments(text)
        self.assertEqual([(ln, b) for ln, b in blocks], [(3, "a comment"), (4, "trailing")])

    def test_docstring(self):
        text = 'def f():\n    """Returns the size."""\n    return 1\n'
        self.assertEqual(dl.extract_comments(text), [(2, "Returns the size.")])

    def test_string_literals_are_not_comments(self):
        text = 'x = "not a comment; really"\n// real\n'
        blocks = dl.extract_comments(text)
        self.assertEqual(blocks, [(2, "real")])

    def test_comment_marker_inside_string_is_ignored(self):
        text = 'url = "http://example.org"  // the url\n'
        self.assertEqual(dl.extract_comments(text), [(1, "the url")])

    def test_rust_and_csharp_doc_markers(self):
        text = "//! crate doc\n/// item doc\n"
        blocks = dl.extract_comments(text)
        self.assertEqual(blocks[0][1], "crate doc\nitem doc")


class JsonStringsTest(unittest.TestCase):
    def test_only_strings_with_spaces(self):
        data = json.dumps({"$schema": "a b", "id": "com.example.id", "msg": "Add a return type.", "n": 3})
        blocks = dl.json_strings(data)
        self.assertEqual([b for _, b in blocks], ["Add a return type."])

    def test_list_of_strings_is_one_block(self):
        data = json.dumps({"lines": ["First line.", "Second line."]})
        self.assertEqual([b for _, b in dl.json_strings(data)], ["First line. Second line."])

    def test_nested_objects(self):
        data = json.dumps({"a": {"b": [{"c": "deep text here"}]}})
        self.assertEqual([b for _, b in dl.json_strings(data)], ["deep text here"])


class StripCodeTest(unittest.TestCase):
    def test_code_span_and_link_become_one_word(self):
        self.assertEqual(dl.strip_code("Use `a; b` and [x](http://e) now."), "Use  CODE  and  CODE  now.")

    def test_placeholder_and_entity(self):
        out = dl.strip_code("`{0}` has a key &middot; here")
        self.assertNotIn("{0}", out)
        self.assertNotIn(";", out)

    def test_html_code_elements(self):
        self.assertNotIn("-", dl.strip_code("Start with <kbd>-</kbd> or <code>a - b</code>."))

    def test_fenced_block_and_tag_first_word(self):
        out = dl.strip_code("Text.\n```\na; b\n```\n@param name the key")
        self.assertNotIn(";", out)
        self.assertNotIn("@param", out)
        self.assertIn("the key", out)
        self.assertEqual(out.count("\n"), 4)

    def test_indented_code_rule_stays_on_one_line(self):
        # A blank line followed by a short indented line isn't one indented code line.
        out = dl.strip_code("Text.\n \n\n   @param name the key")
        self.assertIn("the key", out)

    def test_docstring_body_is_dedented_before_the_indented_code_rule(self):
        out = dl.strip_code("Returns the size.\n\n    The second line; here.\n\n        x = 1\n    ")
        self.assertIn("The second line; here.", out)
        self.assertNotIn("x = 1", out)
        self.assertEqual(out.count("\n"), 5)

    def test_count_words(self):
        self.assertEqual(dl.count_words("Returns the size (in bytes) of `file`."), 6)
        self.assertEqual(dl.count_words(" CODE  is one word"), 4)


class MarkdownBlocksTest(unittest.TestCase):
    def blocks(self, text):
        return [(ln, dl.unmark(b)) for ln, b in dl.markdown_blocks(dedent(text))]

    def test_paragraphs_headings_and_lists(self):
        blocks = self.blocks("""
            # Title

            First paragraph
            continues here.

            - Item one
            - Item two
              continues.
            1. Numbered
            """)
        self.assertEqual(blocks, [
            (1, "Title"),
            (3, "First paragraph\ncontinues here."),
            (6, "Item one"),
            (7, "Item two\ncontinues."),
            (9, "Numbered"),
        ])

    def test_fences_including_nested_and_quoted(self):
        blocks = self.blocks("""
            Before.

            ````md
            ```js
            a; b
            ```
            ````

            > ```css
            > a { x: 1; }
            > ```

            After.
            """)
        self.assertEqual([b for _, b in blocks], ["Before.", "After."])

    def test_indented_code_is_skipped_but_nested_lists_are_read(self):
        blocks = self.blocks("""
            Paragraph.

                code; here

            - Item
                - Nested item
                  continues
            - Next

              Loose paragraph in the item.
            """)
        self.assertEqual([b for _, b in blocks], [
            "Paragraph.", "Item", "Nested item\ncontinues", "Next", "Loose paragraph in the item."])

    def test_table_rows(self):
        blocks = self.blocks("""
            | Use | Instead of |
            |---|---|
            | do | perform, carry out |
            """)
        self.assertEqual(blocks, [(1, "Use Instead of"), (3, "do perform, carry out")])

    def test_rules_and_setext_underlines_are_skipped(self):
        blocks = self.blocks("""
            Title
            =====

            ---

            Text.
            """)
        self.assertEqual([b for _, b in blocks], ["Title", "Text."])

    def test_front_matter_values(self):
        blocks = self.blocks("""
            ---
            name: code-doc-writer
            description: >-
              Write every text a person reads,
              in plain English.
            tags:
              - one word
            versions:
              fpt: '*'
            ---

            Body.
            """)
        self.assertEqual(blocks, [
            (4, "Write every text a person reads,\nin plain English."),
            (7, "one word"),
            (12, "Body."),
        ])

    def test_html_comment_style_block_and_split_tag(self):
        blocks = self.blocks("""
            <!-- a comment
            over two lines; with a semicolon -->

            <style>
              .a { color: red; }
            </style>

            <a
              href="x"
              style="padding: 10px; display: block"
            >
            Text in the link.
            </a>

            Prose.
            """)
        prose = [dl.strip_code(b) for _, b in blocks]
        self.assertFalse(any(";" in p for p in prose), prose)
        self.assertIn("Prose.", prose)

    def test_skipped_lines(self):
        blocks = self.blocks("""
            import Tabs from '@theme/Tabs';
            export const x = 1;

            [ref]: https://example.org "Title"
            <<< @/snippets/file.js{1,3}
            (my-target)=
            :class: tip

            Kept.
            """)
        self.assertEqual([b for _, b in blocks], ["Kept."])

    def test_link_text_is_prose_and_images_are_dropped(self):
        blocks = self.blocks("""
            ![badge](https://img.shields.io/x.svg) Read the [getting started guide](https://e.org) and [the spec][spec].
            """)
        self.assertEqual(blocks[0][1].strip(), "Read the getting started guide and the spec.")

    def test_link_text_is_marked_and_counts_as_one_word(self):
        blocks = dl.markdown_blocks("Read [the full guide](https://e.org) now.")
        self.assertEqual(blocks[0][1], "Read \x02the full guide\x03 now.")
        self.assertEqual(dl.count_words(blocks[0][1]), 3)
        self.assertEqual(dl.unmark(blocks[0][1]), "Read the full guide now.")

    def test_a_link_counts_as_one_word_in_a_markdown_file(self):
        with TempFiles() as t:
            text = "Read [the full guide to timeouts and retries](https://e.org) before the call.\n"
            findings = t.lint("a.md", text, max_words=4)
            self.assertEqual(texts(findings, "long-sentence"), ["5 words: Read the full guide to timeouts and retries before the call."])
            self.assertEqual(texts(t.lint("b.md", text, max_words=5), "long-sentence"), [])

    def test_emphasis_is_stripped(self):
        blocks = self.blocks("**Learn Once:** use _it_ and ==this== and ^^that^^, keep snake_case.")
        self.assertEqual(blocks[0][1], "Learn Once: use it and this and that, keep snake_case.")

    def test_templates_become_one_word_and_keep_line_numbers(self):
        blocks = self.blocks("""
            Use {% data variables.product %} with {{< figure
              src="a.jpg"
              alt="b" >}} and {.class #id} and :material-icon: and ++ctrl+alt++ and {/* note */}.

            Next paragraph.
            """)
        self.assertEqual(blocks[1], (5, "Next paragraph."))
        first = blocks[0][1]
        self.assertEqual(first.count("\n"), 2)
        for leftover in ("{%", "{{", "{.", ":material", "++", "{/*"):
            self.assertNotIn(leftover, first)

    def test_admonitions(self):
        blocks = self.blocks("""
            :::tip Debugging
            Admonition text.
            :::

            !!! note "A quoted title"

                The body of the note.

            === "Tab one"

                Tab body.
            """)
        self.assertEqual([b for _, b in blocks], [
            "Debugging\nAdmonition text.", "A quoted title", "The body of the note.", "Tab one", "Tab body."])

    def test_blockquote_marker_is_stripped(self):
        blocks = self.blocks("> [!NOTE]\n> Quoted text.\n")
        self.assertEqual(blocks[0][1], " CODE \nQuoted text.")


class RulesTest(unittest.TestCase):
    def test_hard_rules_in_source(self):
        with TempFiles() as t:
            f = t.lint("a.kt", """
                // A list; with a semicolon
                // An aside — with an em dash
                // Another aside -- with hyphens
                // A hyphen aside - like this one
                """)
        hard = sorted((x["rule"], x["line"]) for x in f if x["hard"])
        self.assertEqual(hard, [("dash-aside", 4), ("em-dash", 2), ("em-dash", 3), ("semicolon", 1)])

    def test_list_hyphen_is_not_a_dash_aside(self):
        with TempFiles() as t:
            f = t.lint("a.kt", """
                /*
                 * Steps:
                 * - first item
                 * - second item
                 */
                """)
        self.assertNotIn("dash-aside", rules(f))

    def test_code_span_hides_punctuation(self):
        with TempFiles() as t:
            f = t.lint("a.kt", "// Use `a; b - c` here\n")
        self.assertFalse(any(x["hard"] for x in f))

    def test_soft_rules(self):
        with TempFiles() as t:
            f = t.lint("a.py", """
                # Basically, the value is written by the task when adding a check, e.g. this.
                # It cannot utilize the cache under the hood.
                """)
        r = rules(f)
        self.assertIn("word", r)
        self.assertIn("passive?", r)
        self.assertIn("ing-clause", r)
        self.assertIn("contraction", r)
        self.assertIn("figurative?", r)
        self.assertIn("'basically': delete", texts(f, "word"))
        self.assertIn("'e.g.': for example", texts(f, "word"))
        self.assertIn("'utilize': use", texts(f, "word"))
        self.assertIn("'cannot': use 'can't'", texts(f, "contraction"))
        self.assertIn("'under the hood': literal use only", texts(f, "figurative?"))

    def test_state_participles_are_not_passive(self):
        with TempFiles() as t:
            f = t.lint("a.py", "# The option is enabled and the list is sorted.\n")
        self.assertNotIn("passive?", rules(f))

    def test_swap_matches_whole_words_and_inflections(self):
        with TempFiles() as t:
            f = t.lint("a.py", "# A viaduct is not a via. Performance matters. It utilizes and performed.\n")
        self.assertEqual(sorted(texts(f, "word")), ["'perform': do", "'utilize': use", "'via': through, with"])

    def test_is_open_is_not_passive(self):
        with TempFiles() as t:
            f = t.lint("a.py", "# The file is open. The value is then set. The list is written.\n")
        self.assertEqual(texts(f, "passive?"), ["is written"])

    def test_figurative_inflections(self):
        with TempFiles() as t:
            f = t.lint("a.py", "# The change shipped. It bakes the value in. Websites.\n")
        self.assertEqual(sorted(texts(f, "figurative?")), ["'bakes': literal use only", "'shipped': literal use only"])

    def test_code_that_speaks(self):
        with TempFiles() as t:
            f = t.lint("a.py", "# The API tells the caller that the file is missing. The parser said no.\n")
        self.assertEqual(sorted(texts(f, "speaks?")), ["'said': only a person is the actor", "'tells': only a person is the actor"])
        self.assertEqual(texts(f, "figurative?"), [])

    def test_long_sentence_and_max_words(self):
        sentence = "# " + " ".join(["word"] * 22) + ".\n"
        with TempFiles() as t:
            self.assertNotIn("long-sentence", rules(t.lint("a.py", sentence)))
            f = t.lint("b.py", sentence, max_words=20)
        self.assertIn("long-sentence", rules(f))
        self.assertTrue(texts(f, "long-sentence")[0].startswith("22 words:"))

    def test_line_numbers_inside_a_block(self):
        with TempFiles() as t:
            f = t.lint("a.kt", """
                /**
                 * First line.
                 * Second line; here.
                 * Third line utilizes.
                 */
                """)
        self.assertEqual([x["line"] for x in f if x["rule"] == "semicolon"], [3])
        self.assertEqual([x["line"] for x in f if x["rule"] == "word"], [4])

    def test_indented_docstring_is_linted_past_its_first_line(self):
        with TempFiles() as t:
            f = t.lint("a.py", """
                def f():
                    \"\"\"Returns the size.

                    The second line utilizes a word; it has a semicolon.

                        example = f()
                    \"\"\"
                    return 1
                """)
        self.assertEqual([x["line"] for x in f if x["rule"] == "semicolon"], [4])
        self.assertEqual([x["line"] for x in f if x["rule"] == "word"], [4])

    def test_json_file(self):
        with TempFiles() as t:
            f = t.lint("m.json", '{"$schema": "x; y", "id": "a;b", "msg": "The class is open; close it."}')
        self.assertEqual([(x["rule"], x["hard"]) for x in f], [("semicolon", True)])

    def test_markdown_findings_are_soft(self):
        with TempFiles() as t:
            f = t.lint("doc.md", """
                # Title — with a dash

                A sentence; with a semicolon and a word - aside.
                """)
        self.assertEqual(sorted(set(rules(f))), ["dash-aside", "em-dash", "semicolon"])
        self.assertFalse(any(x["hard"] for x in f))

    def test_markdown_entity_and_kbd_pass(self):
        with TempFiles() as t:
            f = t.lint("doc.md", "[A](http://a) &middot; [B](http://b) with <kbd>-</kbd> keys.\n")
        self.assertEqual(rules(f), [])

    def test_mdx_extension(self):
        with TempFiles() as t:
            f = t.lint("page.mdx", "import X from 'y';\n\n<X prop={1}>\n\nText; here.\n\n</X>\n")
        self.assertEqual([(x["rule"], x["line"], x["hard"]) for x in f], [("semicolon", 5, False)])


class CliTest(unittest.TestCase):
    def run_main(self, *argv):
        out = io.StringIO()
        with redirect_stdout(out):
            code = dl.main(["doc_lint.py", *argv])
        return code, out.getvalue()

    def test_exit_codes(self):
        with TempFiles() as t:
            bad = t.write("bad.kt", "// a; b\n")
            soft = t.write("soft.kt", "// Basically fine.\n")
            self.assertEqual(self.run_main(bad)[0], 1)
            self.assertEqual(self.run_main(soft)[0], 0)
            self.assertEqual(self.run_main("--max-words", "20", soft)[0], 0)
        self.assertEqual(self.run_main()[0], 2)

    def test_text_output(self):
        with TempFiles() as t:
            path = t.write("a.kt", "// a; b\n// basically\n")
            code, out = self.run_main(path)
        self.assertEqual(code, 1)
        self.assertIn(f"{path}:1: FAIL semicolon:", out)
        self.assertIn(f"{path}:2: warn word: 'basically': delete", out)
        self.assertIn("1 hard, 1 soft", out)

    def test_json_output(self):
        with TempFiles() as t:
            path = t.write("a.kt", "// a; b\n")
            code, out = self.run_main("--json", path)
        data = json.loads(out)
        self.assertEqual(code, 1)
        self.assertEqual((data["hard"], data["soft"]), (1, 0))
        self.assertEqual(data["findings"][0]["rule"], "semicolon")

    def test_repository_markdown_has_no_hard_failures(self):
        skill = ROOT / "skills" / "code-doc-writer"
        files = [ROOT / "README.md", skill / "SKILL.md", *sorted((skill / "references").glob("*.md"))]
        for path in files:
            findings = dl.lint_file(str(path), dl.MAX_WORDS)
            self.assertFalse([f for f in findings if f["hard"]], path)


class MarkdownCorpusTest(unittest.TestCase):
    """One test for each defect that real READMEs and docs pages exposed."""

    def blocks(self, text):
        return [(ln, dl.unmark(b)) for ln, b in dl.markdown_blocks(dedent(text))]

    def prose(self, text):
        return [dl.strip_code(b) for _, b in self.blocks(text)]

    def test_readme_shape(self):
        # React, Node, Kotlin: badges, an HTML header, a link list, fences, a table, reference definitions.
        blocks = self.blocks("""
            # project

            [![CI](https://img.shields.io/ci.svg)](https://ci.example.org) [![License][badge]][license]

            <p align="center">
              <img src="logo.png" alt="A logo with a semicolon; here">
            </p>

            A tool for building things. Read the [guide](https://example.org/guide).

            - [Install](#install)
            - [Usage](#usage)

            ```sh
            npm install project -- --save; echo done
            ```

            | Option | Meaning |
            |:-------|--------:|
            | `-v`   | Prints the version. |

            [badge]: https://img.shields.io/license.svg
            [license]: LICENSE
            """)
        self.assertEqual([" ".join(dl.strip_code(b).split()) for _, b in blocks], [
            "project",
            "CODE CODE CODE",
            "A tool for building things. Read the guide.",
            "Install",
            "Usage",
            "Option Meaning",
            "CODE Prints the version.",
        ])
        self.assertEqual([ln for ln, _ in blocks], [1, 5, 9, 11, 12, 18, 20])

    def test_badge_inside_a_link_is_dropped(self):
        self.assertEqual(self.blocks("[![CI](https://a/b.svg)](https://ci) done")[0][1].strip(), "done")

    def test_emphasis_after_an_arrow(self):
        # Axios: "Get Security Updates for Axios v0 →**"
        self.assertEqual(self.blocks("**Get updates →**")[0][1], "Get updates →")

    def test_wrapped_reference_link_falls_back_to_code(self):
        # The Rust book wraps a reference link over two lines.
        blocks = self.blocks("""
            As mentioned in the [“Storing Values with
            Variables”][storing-values]<!-- ignore --> section, values are immutable.

            Next.
            """)
        self.assertEqual(blocks[1], (4, "Next."))
        self.assertEqual(dl.strip_code(blocks[0][1]).count("\n"), 1)

    def test_unclosed_fence_skips_the_rest(self):
        self.assertEqual(self.blocks("Text.\n\n```\na; b\nmore\n"), [(1, "Text.")])

    def test_indented_code_in_an_rfc(self):
        # The Rust NLL RFC uses four-space code blocks between paragraphs.
        prose = self.prose("""
            Consider this program:

                let x: &'x i32 = ...; let y = x;
                use(x);

            Here the reference is live.
            """)
        self.assertEqual(prose, ["Consider this program:", "Here the reference is live."])

    def test_html_table_with_split_tags(self):
        # The Axios README has a sponsor table with <a> tags over several lines and a bare ">" line.
        prose = self.prose("""
            <table align="center">
                <tr>
                    <td align="center" width="50%">
                        <a
                            href="https://example.org/?a=1&amp;b=2"
                            style="padding: 10px; display: inline-block"
                            target="_blank"
                        >
                            <img width="90px" src="logo.png" alt="Sponsor" />
                        </a>
                    </td>
                </tr>
            </table>

            Prose after the table.
            """)
        self.assertFalse(any(";" in p or "<" in p for p in prose), prose)
        self.assertIn("Prose after the table.", prose)

    def test_script_svg_and_pre_blocks(self):
        prose = self.prose("""
            <script>
            var a = 1; var b = 2;
            </script>

            <svg viewBox="0 0 1 1">
              <path d="M0 0; L1 1" />
            </svg>

            <pre>
            a; b
            </pre>

            Kept text.
            """)
        self.assertEqual([p for p in prose if p.strip()], ["Kept text."])

    def test_multi_line_jsx_component(self):
        # Next.js and Docusaurus MDX pages use components with props on their own lines.
        prose = self.prose("""
            <Image
              alt="Diagram; with a semicolon"
              srcLight="/light.png"
              width="1600"
            />

            <Tabs>
              <TabItem value="apple" label="Apple">
                This is an apple.
              </TabItem>
            </Tabs>
            """)
        self.assertFalse(any(";" in p for p in prose), prose)
        self.assertTrue(any("This is an apple." in p for p in prose), prose)

    def test_docusaurus_admonition_with_title(self):
        prose = self.prose("""
            :::note[Your Title **with** some _Markdown_ `syntax`!]

            Some **content** with some _Markdown_ `syntax`.

            :::
            """)
        self.assertEqual(prose[1], "Some content with some Markdown  CODE .")
        self.assertNotIn(":::", prose[0])

    def test_liquid_hugo_kramdown_and_math(self):
        # GitHub docs, Hugo docs, Jekyll docs, and the math page.
        prose = self.prose("""
            {% raw %}
            On {% data variables.product.github %} you can write {% octicon "x" aria-label="The icon" %} icons.
            {% endraw %}

            {: .note .warning}
            Using Pygments has been deprecated.

            Use {{% glossary-term shortcode %}} or {{ .Site.Title }} or inline $E = mc^2$ math and
            $$\\sum_{k=1}^n a_k; b$$ display math.

            {{< code-toggle file=hugo >}}
            enableInlineShortcodes = true
            {{< /code-toggle >}}
            """)
        joined = "\n".join(prose)
        for leftover in ("{%", "%}", "{{", "}}", "{:", "$"):
            self.assertNotIn(leftover, joined, joined)
        self.assertIn("Using Pygments has been deprecated.", prose)
        self.assertIn("On  CODE  you can write  CODE  icons.", prose)

    def test_liquid_in_front_matter_values(self):
        blocks = self.blocks("""
            ---
            title: Writing mathematical expressions
            intro: 'Use Markdown on {% data variables.product.github %}.'
            product: '{% data reusables.gated-features.markdown-ui %}'
            versions:
              fpt: '*'
              ghes: '*'
            ---

            Body.
            """)
        self.assertEqual([dl.strip_code(b) for _, b in blocks], [
            "Writing mathematical expressions", "Use Markdown on  CODE .", " CODE ", "Body."])

    def test_mkdocs_admonition_forms(self):
        prose = self.prose("""
            !!! note

                A note without a title.

            ??? example "Expand to show alternate icon sets"

                Collapsible body.

            ???+ tip "Open by default"

                Open body.

            !!! info inline end "Lorem ipsum"

                Inline body.

            === ":octicons-file-code-16: docs/stylesheets/extra.css"

                ``` css
                .md-typeset { color: red; }
                ```

            Prose after.
            """)
        self.assertEqual([p.strip() for p in prose], [
            "A note without a title.",
            "Expand to show alternate icon sets",
            "Collapsible body.",
            "Open by default",
            "Open body.",
            "Lorem ipsum",
            "Inline body.",
            "CODE  docs/stylesheets/extra.css",
            "Prose after.",
        ])

    def test_mkdocs_inline_markup(self):
        prose = self.prose("""
            Press ++ctrl+alt+del++ to see :material-check: and :octicons-arrow-right-16: icons.
            ==This was marked== and ^^this was inserted^^ and ~~this was deleted~~.

            --8<-- "includes/abbreviations.md"
            """)
        self.assertEqual(prose[0], "Press  CODE  to see  CODE  and  CODE  icons.\nThis was marked and this was inserted and this was deleted.")

    def test_myst_directives_roles_and_cards(self):
        prose = self.prose("""
            (syntax/directives)=
            # Directives

            :::{tip}
            :class: myclass1 myclass2
            :name: a-tip-reference
            Let's give readers a helpful hint!
            :::

            ::::{card} Card Title
            Header
            ^^^
            Card content with a {ref}`target` role.
            +++
            Footer
            ::::

            % A MyST comment line is prose to this lint, so it stays.
            """)
        self.assertEqual(prose[:5], [
            "Directives",
            "Let's give readers a helpful hint!",
            " CODE  Card Title\nHeader",
            "Card content with a  CODE  CODE  role.",
            "Footer",
        ])

    def test_quarto_divs_and_heading_ids(self):
        prose = self.prose("""
            ## Headings {#headings}

            ::: {.callout-note appearance="simple"}
            Note text.
            :::

            | Syntax | Output |
            |---|---|
            | `::: {}` text `:::` | ::: {} ::: {} |
            """)
        self.assertEqual(prose[0].strip(), "Headings")
        self.assertEqual(prose[1], "Note text.")
        self.assertNotIn(":::", prose[-1])
        self.assertNotIn("{", prose[-1])

    def test_obsidian_callouts_and_wikilinks(self):
        prose = self.prose("""
            > [!faq]- Are callouts foldable?
            > Yes! In a foldable callout, the contents are hidden.
            > ```css
            > .callout { display: none; }
            > ```

            Link to [[Internal links|a note]] or embed ![[image.png]].
            """)
        self.assertEqual(prose[0], " CODE  Are callouts foldable?\nYes! In a foldable callout, the contents are hidden.")
        self.assertEqual(prose[1], "Link to  CODE ] or embed ! CODE ].")

    def test_vitepress_features(self):
        prose = self.prose("""
            ::: tip Custom Title
            Tip body.
            :::

            <<< @/snippets/snippet.js{1,3}

            [[toc]]

            <Badge type="tip" text="^1.9.0" /> uses `{{ interpolation }}`.
            """)
        self.assertEqual(prose[0], "Custom Title\nTip body.")
        self.assertEqual(prose[-1], " CODE  uses  CODE .")

    def test_label_dash_description_is_a_soft_finding(self):
        # Tokio, markdownlint, awesome-selfhosted: `label - description` list items.
        with TempFiles() as t:
            f = t.lint("doc.md", """
                * tokio 1.48 to 1.53 - Rust 1.71
                * **[MD001](doc/md001.md)** *heading-increment* - Heading levels should only increment by one
                """)
        self.assertEqual([(x["rule"], x["line"], x["hard"]) for x in f if x["rule"] == "dash-aside"],
                         [("dash-aside", 1, False), ("dash-aside", 2, False)])

    def test_finding_line_inside_a_wrapped_paragraph(self):
        with TempFiles() as t:
            f = t.lint("doc.md", """
                # Title

                First line of the paragraph,
                second line; with a semicolon,
                third line utilizes a word.
                """)
        self.assertEqual([(x["rule"], x["line"]) for x in f if x["rule"] in ("semicolon", "word")],
                         [("semicolon", 4), ("word", 5)])

    def test_rst_text_in_a_markdown_file_does_not_crash(self):
        with TempFiles() as t:
            f = t.lint("doc.md", """
                .. _howto-build-docs:

                =========================================
                Building the NumPy API and reference docs
                =========================================

                If you only want to get the documentation, note that pre-built
                versions can be found at

                https://numpy.org/doc/
                """)
        self.assertFalse(any(x["hard"] for x in f))
        self.assertIn("'note that': delete", texts(f, "word"))


if __name__ == "__main__":
    unittest.main()
