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
has a space in it, so identifiers, paths, and URLs pass. A .json file has
a limit of 20 words, or less with --max-words.
Exit code 1 when a hard rule fails.
"""
import json
import re
import sys

MAX_WORDS = 25

# word or phrase -> replacement or "" (delete). STE alternatives, adapted for
# programming: exact computer-science verbs (enable, configure, handle, check,
# register, resolve, return, throw, support) aren't listed because they stay.
SWAPS = {
    "utilize": "use", "utilise": "use", "leverage": "use", "employ": "use",
    "perform": "do", "carry out": "do", "execute": "run", "invoke": "call",
    "ensure": "make sure", "verify": "check or make sure", "guarantee": "make sure",
    "obtain": "get", "retrieve": "get", "acquire": "get", "fetch": "get (unless a git fetch)",
    "determine": "find", "locate": "find", "discover": "find",
    "indicate": "show", "represent": "show or stand for", "denote": "show", "signify": "show",
    "facilitate": "help", "assist": "help",
    "provide": "give", "supply": "give", "furnish": "give",
    "allow": "let", "permit": "let",
    "assume": "think or expect", "consider": "think",
    "comprise": "have", "consist of": "have", "constitute": "be",
    "commence": "start", "initiate": "start", "terminate": "stop", "cease": "stop",
    "modify": "change", "alter": "change", "adjust": "change",
    "approximately": "about", "additionally": "also", "furthermore": "also", "moreover": "also",
    "however": "but", "nevertheless": "but", "nonetheless": "but",
    "therefore": "thus", "hence": "thus", "consequently": "thus",
    "subsequently": "then", "afterwards": "then", "whilst": "while",
    "via": "through", "within": "in", "upon": "on", "amongst": "among",
    "prior to": "before", "subsequent to": "after", "in order to": "to",
    "so as to": "to", "as well as": "and", "in addition to": "and", "along with": "and",
    "due to the fact that": "because", "owing to": "because", "since": "because (if causal)",
    "in the event that": "if", "in case": "if", "in the case of": "for",
    "with regard to": "about", "with respect to": "about", "regarding": "about",
    "in terms of": "", "a number of": "some", "a variety of": "different",
    "various": "different", "numerous": "many", "multiple": "many or several",
    "is able to": "can", "has the ability to": "can", "is capable of": "can",
    "it is possible to": "can", "may": "can", "might": "can", "could": "can",
    "should": "must, or delete", "ought to": "must",
    "appropriate": "applicable", "relevant": "related", "respective": "",
    "respectively": "", "particular": "", "certain": "some",
    "desired": "", "corresponding": "related or matching",
    "the following": "these", "as follows": "", "aforementioned": "", "said": "",
    "e.g.": "for example", "i.e.": "that is", "etc.": "", "etc": "", "vs.": "or", "cf.": "compare",
    "note that": "", "please note": "", "it is worth noting": "", "it should be noted": "",
    "notably": "", "importantly": "", "interestingly": "", "unfortunately": "",
    "basically": "", "simply": "", "just": "", "actually": "", "essentially": "",
    "effectively": "", "really": "", "very": "", "quite": "", "rather": "",
    "obviously": "", "of course": "", "clearly": "", "naturally": "",
    "deliberately": "", "on purpose": "", "intentionally": "", "by design": "",
    "honest": "", "honestly": "", "meant for": "for", "meant to": "",
    "in other words": "", "that is to say": "", "needless to say": "",
    "in this way": "", "at this point": "", "currently": "", "at the moment": "",
    "keep in mind": "", "bear in mind": "", "make sure to": "",
    "which is why": "thus", "which means that": "so", "so that": "so, or to",
    "in such a way that": "so", "to the extent that": "if",
    "there is": "restructure", "there are": "restructure",
    "a.k.a.": "also", "aka": "also", "say,": "for example",
}

HARD_PATTERNS = [
    ("semicolon", re.compile(r";")),
    ("em-dash", re.compile(r"[—–]| -- ")),
    # A hyphen with a space on each side, inside a sentence, is a dash aside. A list item starts its line with a hyphen.
    ("dash-aside", re.compile(r"(?<=[\w,.)]) - (?=\w)")),
]

# Words that are usually figurative in code docs. Literal use is fine.
FIGURATIVE = [
    "bake", "baked", "bakes", "travel", "travels", "live", "lives", "land", "lands",
    "ship", "ships", "shipped", "surface", "surfaces", "bubble", "bubbles", "swallow",
    "swallows", "guard", "guards", "wire", "wires", "wired", "plumb", "spell out",
    "spelled out", "spelling out", "fall back", "falls back", "under the hood",
    "out of the box", "stand in", "stands in", "stand-in", "pick up", "picks up",
    "kick in", "kicks in", "kick off", "kicks off", "fire", "fires", "world", "flavor",
    "blessed", "sane", "sanity", "happy path", "magic", "glue", "plumbing", "footgun",
    "gotcha", "boils down", "at the end of the day", "in a nutshell", "on the fly",
    "come into play", "comes into play", "take care of", "takes care of", "hand off",
    "hands off", "handed off", "gate", "gates", "gated", "funnel", "funnels", "wrap up",
    "wraps up", "roll up", "rolls up", "walk", "walks", "sits", "sit on top", "umbrella",
    "lightweight", "heavy lifting", "first class", "first-class", "citizen", "sibling",
    "cousin", "stale", "fresh", "sweep", "sweeps", "bleed", "bleeds", "leak", "leaks",
    "poison", "pollute", "pollutes", "hijack", "steal", "steals", "promote", "demote",
    "demoted", "promoted", "honor", "honors", "honour", "honours", "respect", "respects",
    "aware", "friendly", "smart", "dumb", "naive", "clever", "trick", "tricks", "hack",
    "pay", "pays", "paid", "afford", "affords",
    "invite", "invites", "go through", "goes through", "pull in", "pulls in",
    "hot path", "escape hatch", "through the lens", "bridge", "bridges",
]
FIG_RE = re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in FIGURATIVE) + r")(?![\w-])", re.I)

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
    blocks = json_strings(text) if path.endswith(".json") else extract_comments(text)
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
        for word, repl in SWAPS.items():
            pat = r"(?<![\w-])" + re.escape(word) + r"(?![\w-])"
            for m in re.finditer(pat, lower):
                ln = line + prose.lower()[:max(0, m.start())].count("\n")
                hint = f"use '{repl}'" if repl and repl != "restructure" else ("restructure" if repl == "restructure" else "delete")
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
        limit = min(max_words, 20) if f.endswith(".json") else max_words
        all_findings.extend(lint_file(f, limit))
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
