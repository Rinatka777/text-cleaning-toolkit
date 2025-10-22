from __future__ import annotations

import re

_WS_RE = re.compile(r"\s+")
_NON_WORD_SPACE = re.compile(r"(?:[^\w\s]|_)", flags=re.UNICODE)
_NUM_RE = re.compile(r"\d+", flags=re.UNICODE)
TOKEN_RE = re.compile(r"<[A-Z0-9_]+>")

def to_lower(s: str) -> str:
    parts: list[str] = []
    i = 0
    for m in TOKEN_RE.finditer(s):
        parts.append(s[i:m.start()].lower())
        parts.append(m.group(0))  # keep token as-is
        i = m.end()
    parts.append(s[i:].lower())
    return "".join(parts)

def normalize_whitespace(s: str) -> str:
    s2 = _WS_RE.sub(" ", s)
    return s2.strip()

def strip_punctuation(s: str) -> str:
    parts: list[str] = []
    i = 0
    for m in TOKEN_RE.finditer(s):
        cleaned = _NON_WORD_SPACE.sub(" ", s[i:m.start()])
        parts.append(cleaned)
        parts.append(m.group(0))
        i = m.end()
    parts.append(_NON_WORD_SPACE.sub(" ", s[i:]))
    return normalize_whitespace("".join(parts))

def remove_stopwords(s: str, stopwords: set[str]) -> str:
    if s is None:
        return s
    tokens = s.split()
    kept = []
    for t in tokens:
        if t not in stopwords:
            kept.append(t)
    return " ".join(kept)

def replace_digits(s: str, token: str = "<NUM>") -> str:
    return _NUM_RE.sub(token, s)


