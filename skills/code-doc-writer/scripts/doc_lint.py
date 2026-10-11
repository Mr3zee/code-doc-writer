#!/usr/bin/env python3
"""Lint the comments and doc comments of source files.

Hard failures (exit code 1): a semicolon, an em dash, an en dash, ` -- `,
or a ` - ` aside. Soft warnings: a long sentence, a filler word, a word
with a plainer swap, a Latin abbreviation, a figurative word, a likely
passive, an "-ing" clause, and an uncontracted negative. Works on any
language that uses /* */, //, # or triple-quoted strings.

Usage:
    doc_lint.py [--json] [--max-words N] FILE...
The lint reads a .json file as data and lints every string value that
has a space in it, so identifiers, paths, and URLs pass.
The lint reads a .md file as prose: each paragraph, heading, list item,
and table row is one block. Fenced code is skipped. To lint a text that
isn't a comment, such as one message or a string in a source file, put
it in a temporary .md file and lint that file.
The word lists come from references/words.md next to this script's
directory: the two swap tables, the delete list, and the figurative list.
Exit code 1 when a hard rule fails.
"""
import json
import re
import sys
from pathlib import Path

MAX_WORDS = 25

WORDS_FILE = Path(__file__).resolve().parent.parent / "references" / "words.md"


def split_items(cell):
    """Split "a, b (condition), c" into (word, condition) pairs."""
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
    """Return (swaps, figurative) from words.md. swaps maps a word to its hint."""
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
    """Return the regular inflections of the first word of a phrase."""
    head, _, rest = phrase.partition(" ")
    forms = {head}
    if head.endswith("e"):
        forms.update({head + "s", head + "d", head[:-1] + "ing"})
    elif re.search(r"[^aeiou]y$", head):
        forms.update({head[:-1] + "ies", head[:-1] + "ied", head + "ing"})
    else:
        forms.update({head + "s", head + "es", head + "ed", head + "ing"})
        if re.search(r"[^aeiou][aeiou][^aeiouwxy]$", head):
            forms.update({head + head[-1] + "ed", head + head[-1] + "ing"})
    return {f + (" " + rest if rest else "") for f in forms}


if not WORDS_FILE.is_file():
    sys.exit(f"doc_lint.py: {WORDS_FILE} is missing")
SWAPS, FIGURATIVE = load_words(WORDS_FILE)
SWAP_RE = {word: re.compile(r"(?<![\w-])" + re.escape(word.rstrip(".")) + r"\.?(?![\w-])") for word in SWAPS}
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
               "bound", "fixed", "limited", "related", "used", "known", "expected"}

PASSIVE = re.compile(
    r"\b(is|are|was|were|be|been|being|gets|get|got)\s+(\w+ed|\w+en|built|done|made|kept|held|"
    r"run|set|put|read|written|given|taken|seen|known|shown|found|thrown|caught|sent|left|lost|"
    r"hidden|chosen|driven|bound|cut|hit|split|spread)\b", re.I)
ING_CLAUSE = re.compile(r"\b(when|while|by|before|after|without|upon|on|for|instead of)\s+\w+ing\b", re.I)

CODE_SPAN = re.compile(r"`[^`]*`|\[[^\]]*\]\([^)]*\)|\[[^\]]*\]|\{@\w+[^}]*\}|<[^>]+>")
SENT_SPLIT = re.compile(r"(?<=[.!?:])\s+(?=[A-Z0-9`\[(\"'])")


def extract_comments(text):
    """Return (line_number, comment_text) pairs, one for each comment block."""
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
    """Return (line, prose) pairs for the string values of a JSON document. A list of strings is one pair."""
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
MD_RULE = re.compile(r"^(---+|\*\*\*+|___+|\|?\s*:?-{3,}[-|:\s]*)$")


def markdown_blocks(text):
    """Return (line, prose) pairs for a Markdown document.

    A paragraph, a heading, a list item, or a table row is one block. A
    fenced code block, a rule, and a table separator row are skipped.
    """
    out = []
    buf, start = [], [0]
    in_fence = False

    def flush():
        if buf:
            out.append((start[0], "\n".join(buf)))
        buf.clear()

    for i, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = not in_fence
            flush()
            continue
        if in_fence:
            continue
        if not s or MD_RULE.match(s):
            flush()
            continue
        ln = raw.lstrip()
        m = MD_MARKER.match(ln)
        if m:
            flush()
            ln = ln[m.end():]
            start[0] = i
        elif s.startswith("|"):
            flush()
            ln = " ".join(c.strip() for c in s.strip("|").split("|"))
            start[0] = i
        elif not buf:
            start[0] = i
        buf.append(ln)
        if m and m.group(1).startswith("#") or s.startswith("|"):
            flush()
    flush()
    return out


def strip_code(comment):
    """Drop fenced code and shorten code spans so they count as one word."""
    comment = re.sub(r"```.*?```", " ", comment, flags=re.S)
    comment = re.sub(r"^\s{4,}\S.*$", " ", comment, flags=re.M)  # indented code
    comment = re.sub(r"^\s*@\w+\s+\S+", " ", comment, flags=re.M)  # drop the tag and its first word, keep the rest
    comment = re.sub(r"\{\d+\}", " PARAM ", comment)
    return CODE_SPAN.sub(" CODE ", comment)


def count_words(sentence):
    s = re.sub(r"\([^)]*\)", " PAREN ", sentence)
    return len([w for w in re.split(r"\s+", s.strip()) if w and re.search(r"\w", w)])


def lint_file(path, max_words):
    text = open(path, encoding="utf-8", errors="replace").read()
    findings = []
    if path.endswith(".json"):
        blocks = json_strings(text)
    elif path.endswith((".md", ".markdown")):
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
                findings.append(dict(file=path, line=ln, rule=name, hard=True,
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
