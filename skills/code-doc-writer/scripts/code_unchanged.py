#!/usr/bin/env python3
"""Compare two source files with all comments removed. Exit 1 when the code differs.

Usage: code_unchanged.py ORIGINAL REWRITTEN
"""
import re
import sys
import difflib


def strip(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"(^|[^:\"'])//[^\n]*", r"\1", text)
    text = re.sub(r"^\s*#(?!!)[^\n]*$", "", text, flags=re.M)
    text = re.sub(r'"""(?:.|\n)*?"""', "", text)
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    return lines


a, b = (strip(open(p, encoding="utf-8").read()) for p in sys.argv[1:3])
if a == b:
    print("code unchanged")
    sys.exit(0)
for d in difflib.unified_diff(a, b, "original", "rewritten", lineterm="", n=1):
    print(d)
sys.exit(1)
