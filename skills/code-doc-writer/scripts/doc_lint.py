#!/usr/bin/env python3
"""Lints the prose in source comments, JSON strings, and Markdown files.

Usage:
    doc_lint.py [--json] [--max-words N] FILE...

Hard failures (exit code 1): a semicolon, an em dash, an en dash, ` -- `,
or a ` - ` aside. Soft warnings: a long sentence, a filler word, a word
with a plainer swap, a Latin abbreviation, a figurative word, a likely
passive, an "-ing" clause, and an uncontracted negative.

A source file: the lint reads the /* */, //, and # comments and the
triple-quoted strings. It doesn't read string literals. Any language
with these comment markers works.
A .json file: the lint reads every string value that has a space in it,
so identifiers, paths, and URLs pass.
A .md file: the lint reads each paragraph, heading, list item, table row,
and front matter value as one block. It skips code blocks, HTML tags and
comments, images, template calls, and link reference definitions. It
reads the text of a link as prose. Every finding is a soft warning,
because the lint can't tell prose from markup it doesn't know.
To lint one message or a string, put it in a temporary .md file.

The word lists come from references/words.md next to the scripts
directory: the two swap tables, the delete list, and the figurative list.
"""
import json
import re
import sys
from pathlib import Path

MAX_WORDS = 25

WORDS_FILE = Path(__file__).resolve().parent.parent / "references" / "words.md"


def split_items(cell):
    """Splits "a, b (condition), c" into (word, condition) pairs."""
    items, depth, buf = [], 0, ""
    for ch in cell:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            items.append(buf)
            buf = ""
        else:
            buf += ch
    items.append(buf)
    out = []
    for item in items:
        m = re.match(r"\s*(.*?)\s*(\([^)]*\))?\s*$", item)
        word = m.group(1).strip().strip('"').lower()
        if word:
            out.append((word, " " + m.group(2) if m.group(2) else ""))
    return out


def load_words(path):
    """Returns (swaps, figurative) from words.md. swaps maps a word to its hint."""
    swaps, figurative = {}, []
    section = ""
    bullets = []

    def flush():
        for text in bullets:
            if section.startswith("words to delete"):
                for word, _ in split_items(text):
                    swaps[word] = "delete"
            elif section.startswith("often figurative"):
                figurative.extend(word for word, _ in split_items(text))
        bullets.clear()

    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            flush()
            section = ln[3:].strip().lower()
        elif ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) != 2 or cells[0] in ("Use", "Replace") or set(cells[0]) <= set("-"):
                continue
            if section.startswith("plain verbs"):
                for word, cond in split_items(cells[1]):
                    swaps[word] = cells[0] + cond
            elif section.startswith("words with a plainer swap"):
                for word, cond in split_items(cells[0]):
                    swaps[word] = cells[1] + cond
        elif ln.startswith("- "):
            bullets.append(ln[2:])
        elif ln.startswith("  ") and bullets:
            bullets[-1] += " " + ln.strip()
        else:
            flush()
    flush()
    return swaps, figurative


def word_forms(phrase):
    """Returns the regular inflections of the first word of a phrase."""
    head, _, rest = phrase.partition(" ")
    forms = {head}
    if head.endswith("e"):
        forms.update({head + "s", head + "d", head[:-1] + "ing"})
    elif re.search(r"[^aeiou]y$", head):
        forms.update({head[:-1] + "ies", head[:-1] + "ied", head + "ing"})
    else:
        forms.update({head + "s", head + "ed", head + "ing"})
        if re.search(r"(s|x|z|ch|sh|o)$", head):
            forms.add(head + "es")
        if re.search(r"[^aeiou][aeiou][^aeiouwxy]$", head):
            forms.update({head + head[-1] + "ed", head + head[-1] + "ing"})
    return {f + (" " + rest if rest else "") for f in forms}


if not WORDS_FILE.is_file():
    sys.exit(f"doc_lint.py: {WORDS_FILE} is missing")
SWAPS, FIGURATIVE = load_words(WORDS_FILE)
SWAP_RE = {word: re.compile(r"(?<![\w-])(" + "|".join(re.escape(f.rstrip(".")) for f in sorted(word_forms(word), key=len, reverse=True)) + r")\.?(?![\w-])") for word in SWAPS}
FIG_FORMS = sorted({f for w in FIGURATIVE for f in word_forms(w)}, key=len, reverse=True)
FIG_RE = re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in FIG_FORMS) + r")(?![\w-])", re.I)

HARD_PATTERNS = [
    ("semicolon", re.compile(r";")),
    ("em-dash", re.compile(r"[—–]| -- ")),
    # A hyphen with a space on each side, inside a sentence, is a dash aside. A list item starts its line with a hyphen.
    ("dash-aside", re.compile(r"(?<=[\w,.)]) - (?=\w)")),
]

CONTRACT = {"cannot": "can't", "do not": "don't", "does not": "doesn't", "is not": "isn't",
            "will not": "won't", "did not": "didn't", "are not": "aren't", "was not": "wasn't"}
CONTRACT_RE = re.compile(r"\b(" + "|".join(CONTRACT) + r")\b", re.I)

# Participles that name a state, not an action. "is enabled" is a state.
STATE_WORDS = {"enabled", "disabled", "deprecated", "supported", "unsupported", "required", "configured",
               "installed", "published", "applied", "registered", "resolved", "selected", "set", "defined",
               "declared", "annotated", "marked", "named", "based", "intended", "allowed", "permitted",
               "documented", "undocumented", "sorted", "cached", "locked", "closed", "connected", "nested",
               "bound", "fixed", "limited", "related", "used", "known", "expected",
               # Not participles, but they end in "en" or "ed".
               "open", "even", "often", "then", "when", "ten", "seven", "eleven", "green", "golden", "red"}

PASSIVE = re.compile(
    r"\b(is|are|was|were|be|been|being|gets|get|got)\s+(\w+ed|\w+en|built|done|made|kept|held|"
    r"run|set|put|read|written|given|taken|seen|known|shown|found|thrown|caught|sent|left|lost|"
    r"hidden|chosen|driven|bound|cut|hit|split|spread)\b", re.I)
ING_CLAUSE = re.compile(r"\b(when|while|by|before|after|without|upon|on|for|instead of)\s+\w+ing\b", re.I)

CODE_SPAN = re.compile(r"`[^`]*`|<(code|kbd|samp|var|tt)>.*?</\1>|\[[^\]]*\]\([^)]*\)|\[[^\]]*\]|\{@\w+[^}]*\}|<[^>]+>", re.S)
SENT_SPLIT = re.compile(r"(?<=[.!?:])\s+(?=[A-Z0-9`\[(\"'])")


def extract_comments(text):
    """Returns (line_number, comment_text) pairs, one for each comment block."""
    i, n, line = 0, len(text), 1
    out = []
    while i < n:
        c = text[i]
        two = text[i:i + 2]
        three = text[i:i + 3]
        if three in ('"""', "'''"):
            j = text.find(three, i + 3)
            if j < 0:
                break
            body = text[i + 3:j]
            out.append((line, body))
            line += text[i:j + 3].count("\n")
            i = j + 3
        elif two == "/*":
            j = text.find("*/", i + 2)
            if j < 0:
                break
            body = text[i + 2:j]
            body = "\n".join(re.sub(r"^\s*\*+ ?", "", ln) for ln in body.splitlines())
            out.append((line, body))
            line += text[i:j + 2].count("\n")
            i = j + 2
        elif two == "//" or (c == "#" and text[i:i + 2] != "#!" and (i == 0 or text[i - 1] in " \t\n")):
            start_line = line
            buf = []
            while i < n:
                j = text.find("\n", i)
                if j < 0:
                    j = n
                ln = text[i:j]
                buf.append(re.sub(r"^\s*(//[/!]?|#+)\s?", "", ln))
                i = j + 1
                line += 1
                # continue only if the next line is also a line comment
                k = i
                while k < n and text[k] in " \t":
                    k += 1
                if not (text[k:k + 2] == "//" or text[k:k + 1] == "#"):
                    break
            out.append((start_line, "\n".join(buf)))
        elif c in "\"'":
            j = i + 1
            while j < n and text[j] != c:
                if text[j] == "\\":
                    j += 1
                if text[j] == "\n":
                    break
                j += 1
            line += text[i:j + 1].count("\n")
            i = j + 1
        else:
            if c == "\n":
                line += 1
            i += 1
    return out


def json_strings(text):
    """Returns (line, prose) pairs for the string values of a JSON document. A list of strings is one pair."""
    data = json.loads(text)
    out = []

    def line_of(snippet):
        i = text.find(snippet[:40].replace("\\", "\\\\").replace('"', '\\"'))
        return text[:i].count("\n") + 1 if i >= 0 else 1

    def is_prose(text):
        # An identifier, a path, or a URL has no space. Prose has spaces.
        return " " in text.strip()

    def walk(v):
        if isinstance(v, str):
            if is_prose(v):
                out.append((line_of(v), v))
        elif isinstance(v, list):
            if v and all(isinstance(x, str) for x in v):
                joined = " ".join(v)
                if is_prose(joined):
                    out.append((line_of(v[0]), joined))
            else:
                for x in v:
                    walk(x)
        elif isinstance(v, dict):
            for k, x in v.items():
                if k == "$schema":
                    continue
                walk(x)
    walk(data)
    return out


MD_MARKER = re.compile(r"^(#{1,6}\s+|[-*+]\s+|\d+[.)]\s+|>\s*)")
MD_RULE = re.compile(r"^(---+|\*\*\*+|___+|={3,}|\^{3,}|\+{3,}|\|?\s*:?-{3,}[-|:\s]*)$")
# Skipped lines: a link reference definition, an MDX import or export, a bare admonition fence,
# an attribute list, a VitePress include, a MyST target, a MyST directive option.
MD_SKIP = re.compile(r"^(\[[^\]]+\]:\s|import\s|export\s|:::+\s*$|\{[.:#][^}]*\}\s*$|<<<\s|\(\S+\)=$|:[\w-]+:\s)")
MD_ADMONITION_BLOCK = re.compile(r'^(!!!|\?\?\?\+?|===)\s+(?:[\w+-]+\s+)*"?([^"]*)"?\s*$')  # MkDocs admonition or content tab
MD_HTML_BLOCK = re.compile(r"^<(style|script|svg|pre)\b", re.I)
MD_FENCE = re.compile(r"^(`{3,}|~{3,})")
MD_IMAGE = re.compile(r"!\[[^\]\n]*\]\([^)\n]*\)|!\[[^\]\n]*\]\[[^\]\n]*\]")
MD_ATTR = re.compile(r"\{[.:#][^}]*\}")  # an attribute list such as {#id}, {.class}, or {: .note}. It isn't a word.
MD_LINK = re.compile(r"\[([^\]\n]+)\]\([^)\n]*\)|\[([^\]\n]+)\]\[[^\]\n]*\]")
MD_EMPHASIS = re.compile(r"(?<!\w)(\*{1,2}|_{1,2}|~{1,2}|==|\^\^)(?=[\w(\[`\"'])|(?<=\S)(\*{1,2}|_{1,2}|~{1,2}|==|\^\^)(?=\s|$|[.,:;!?)])")
# Markup that reads as one word. A Hugo shortcode, a Liquid tag, a Mustache expression, an MDX comment
# or expression, an attribute list, a MyST role, math, an icon or emoji code, a key combination.
MD_TEMPLATE = re.compile(
    r"\{\{<.*?>\}\}|\{\{%.*?%\}\}|\{\{.*?\}\}|\{%.*?%\}|\{/\*.*?\*/\}|\{[\w.-]*\}|\[!\w+\][-+]?|"
    r"\$\$.*?\$\$|(?<!\w)\$[^$\n]+\$(?!\w)|(?<!\w):[\w+-]+:(?!\w)|\+\+\S+?\+\+|:{3,}", re.S)
MD_ADMONITION = re.compile(r"^:::+\s*\w*\s*")
FRONT_KEY = re.compile(r"^([\w-]+):\s*(.*)$")


def markdown_prose(line):
    """Removes images and emphasis marks, unwraps link text, and replaces template calls with CODE."""
    line = MD_ADMONITION.sub("", line)
    line = MD_ATTR.sub("", line)
    line = MD_IMAGE.sub(" ", line)
    line = MD_LINK.sub(lambda m: m.group(1) or m.group(2), line)
    line = MD_TEMPLATE.sub(" CODE ", line)
    return MD_EMPHASIS.sub("", line)


def markdown_blocks(text):
    """Returns (line, prose) pairs for a Markdown document.

    A paragraph, a heading, a list item, a table row, or a front matter value
    is one block. The lint skips a fenced or indented code block, an HTML
    comment, a rule, a table separator row, and a link reference definition.
    """
    out = []
    buf, start = [], [0]
    fence = ""
    in_comment = False
    html_block = ""  # the closing tag of an open <style>, <script>, <svg>, or <pre>
    in_quote = False
    list_indent = None  # the content column of the last list item
    lines = text.splitlines()
    front = 0
    if lines and lines[0].strip() == "---":
        front = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)

    def flush():
        if buf and any(w.strip() for w in buf):
            # A template call can span lines. Keep its newlines so line numbers stay right.
            block = MD_TEMPLATE.sub(lambda m: " CODE " + "\n" * m.group(0).count("\n"), "\n".join(buf))
            out.append((start[0], block))
        buf.clear()

    for i, raw in enumerate(lines, 1):
        s = raw.strip()
        if i <= front + 1 and front:
            # Front matter: one block for each value that has a space. A folded scalar continues on indented lines.
            m = FRONT_KEY.match(raw)
            if s == "---" or (m and m.group(2) in ("", ">", ">-", "|", "|-")):
                flush()
                start[0] = i
            elif m:
                flush()
                start[0] = i
                value = m.group(2).strip().strip("'\"")
                if " " in value:
                    buf.append(markdown_prose(value))
                    flush()
            elif raw[:1] in " \t" or s.startswith("- "):
                nested = FRONT_KEY.match(s)
                if nested and " " not in nested.group(2):
                    continue  # a nested key with an identifier value
                if not buf:
                    start[0] = i
                buf.append(markdown_prose(s[2:] if s.startswith("- ") else s))
            continue
        if in_comment:
            if "-->" in s:
                in_comment = False
            continue
        if s.startswith("<!--") and "-->" not in s:
            flush()
            in_comment = True
            continue
        if html_block:
            if html_block in s.lower():
                html_block = ""
            continue
        m = MD_HTML_BLOCK.match(s)
        if m and f"</{m.group(1).lower()}>" not in s.lower():
            flush()
            html_block = f"</{m.group(1).lower()}>"
            continue
        m = MD_FENCE.match(re.sub(r"^(>\s*)+", "", s))  # a fence in a blockquote
        if m and not fence:
            fence = m.group(1)
            flush()
            continue
        if fence:
            # A fence closes only on the same character with at least the opening length.
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = ""
            continue
        bare = MD_ADMONITION.sub("", s)
        if not s or MD_RULE.match(s) or MD_SKIP.match(s) or MD_TEMPLATE.fullmatch(bare) or MD_ATTR.fullmatch(bare):
            flush()
            in_quote = False
            continue
        indent = len(raw.expandtabs(4)) - len(raw.expandtabs(4).lstrip())
        if not buf and indent >= (list_indent or 0) + 4:
            continue  # an indented code block
        ln = raw.lstrip()
        m = MD_ADMONITION_BLOCK.match(ln)
        if m:
            flush()
            start[0] = i
            list_indent = indent + 4  # the body has four more spaces of indentation
            if " " in m.group(2):
                buf.append(markdown_prose(m.group(2)))
                flush()
            continue
        m = MD_MARKER.match(ln)
        if m and m.group(1).startswith(">") and buf and "".join(buf).count("<") > "".join(buf).count(">"):
            m = None  # the ">" closes a multi-line HTML tag
        ln = markdown_prose(ln)
        quote = bool(m) and m.group(1).startswith(">")
        if m:
            if not (quote and in_quote):
                flush()
                start[0] = i
            ln = markdown_prose(raw.lstrip()[m.end():])
            if m.group(1).startswith("#"):
                list_indent = None
            elif not quote:
                list_indent = indent + len(m.group(1))
        elif s.startswith("|"):
            flush()
            ln = " ".join(c.strip() for c in markdown_prose(s).strip("|").split("|"))
            start[0] = i
        elif not buf:
            start[0] = i
            if indent == 0:
                list_indent = None
        if not ln.strip():
            flush()  # the line held only markup
            continue
        in_quote = quote
        buf.append(ln)
        if m and m.group(1).startswith("#") or s.startswith("|"):
            flush()
    flush()
    return out


def dedent_body(comment):
    """Removes the indentation that every line after the first shares.

    A docstring inside a function has the indentation of the function body, so the
    indented-code rule skips its lines without this step. The first line starts
    right after the quotes, so it has no part in the margin.
    """
    lines = comment.split("\n")
    body = [ln for ln in lines[1:] if ln.strip()]
    if not body:
        return comment
    margin = min(len(ln) - len(ln.lstrip(" \t")) for ln in body)
    return "\n".join(lines[:1] + [ln[margin:] if ln.strip() else ln for ln in lines[1:]])


def strip_code(comment):
    """Removes fenced code and shortens each code span to one word."""
    comment = dedent_body(comment)
    comment = re.sub(r"```.*?```", lambda m: " " + "\n" * m.group(0).count("\n"), comment, flags=re.S)
    comment = re.sub(r"^[ \t]{4,}\S.*$", " ", comment, flags=re.M)  # indented code
    comment = re.sub(r"^[ \t]*@\w+[ \t]+\S+", " ", comment, flags=re.M)  # remove the tag and its first word, keep the rest
    comment = re.sub(r"\{\d+\}", " PARAM ", comment)
    comment = re.sub(r"&[#\w]+;", " ", comment)  # an HTML entity such as &middot;
    return CODE_SPAN.sub(lambda m: " CODE " + "\n" * m.group(0).count("\n"), comment)


def count_words(sentence):
    s = re.sub(r"\([^)]*\)", " PAREN ", sentence)
    return len([w for w in re.split(r"\s+", s.strip()) if w and re.search(r"\w", w)])


def lint_file(path, max_words):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    findings = []
    markdown = path.endswith((".md", ".markdown", ".mdx"))
    if path.endswith(".json"):
        blocks = json_strings(text)
    elif markdown:
        blocks = markdown_blocks(text)
    else:
        blocks = extract_comments(text)
    for line, raw in blocks:
        if not raw.strip():
            continue
        prose = strip_code(raw)
        for name, pat in HARD_PATTERNS:
            for m in pat.finditer(prose):
                ln = line + prose[:m.start()].count("\n")
                findings.append(dict(file=path, line=ln, rule=name, hard=not markdown,
                                     text=prose[max(0, m.start() - 30):m.end() + 30].replace("\n", " ").strip()))
        flat = re.sub(r"\s+", " ", prose).strip()
        for sent in SENT_SPLIT.split(flat):
            n = count_words(sent)
            if n > max_words:
                findings.append(dict(file=path, line=line, rule="long-sentence", hard=False,
                                     text=f"{n} words: {sent[:120]}"))
        lower = " " + re.sub(r"\s+", " ", prose.lower()) + " "
        for word, hint in SWAPS.items():
            for m in SWAP_RE[word].finditer(lower):
                ln = line + prose.lower()[:max(0, m.start())].count("\n")
                findings.append(dict(file=path, line=ln, rule="word", hard=False,
                                     text=f"'{word}': {hint}"))
        for m in CONTRACT_RE.finditer(prose):
            ln = line + prose[:m.start()].count("\n")
            findings.append(dict(file=path, line=ln, rule="contraction", hard=False,
                                 text=f"'{m.group(0)}': use '{CONTRACT[m.group(0).lower()]}'"))
        for m in FIG_RE.finditer(prose):
            ln = line + prose[:m.start()].count("\n")
            findings.append(dict(file=path, line=ln, rule="figurative?", hard=False,
                                 text=f"'{m.group(0)}': literal use only"))
        for m in PASSIVE.finditer(prose):
            if m.group(2).lower() in STATE_WORDS:
                continue
            ln = line + prose[:m.start()].count("\n")
            findings.append(dict(file=path, line=ln, rule="passive?", hard=False, text=m.group(0)))
        for m in ING_CLAUSE.finditer(prose):
            ln = line + prose[:m.start()].count("\n")
            findings.append(dict(file=path, line=ln, rule="ing-clause", hard=False, text=m.group(0)))
    return findings


def main(argv):
    as_json = "--json" in argv
    max_words = MAX_WORDS
    files = []
    it = iter(a for a in argv[1:] if a != "--json")
    for a in it:
        if a == "--max-words":
            max_words = int(next(it))
        else:
            files.append(a)
    if not files:
        print(__doc__)
        return 2
    all_findings = []
    for f in files:
        all_findings.extend(lint_file(f, max_words))
    hard = [x for x in all_findings if x["hard"]]
    if as_json:
        print(json.dumps(dict(findings=all_findings, hard=len(hard), soft=len(all_findings) - len(hard)), indent=1))
    else:
        for x in all_findings:
            flag = "FAIL" if x["hard"] else "warn"
            print(f"{x['file']}:{x['line']}: {flag} {x['rule']}: {x['text']}")
        print(f"\n{len(hard)} hard, {len(all_findings) - len(hard)} soft")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
