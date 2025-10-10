from __future__ import annotations

import re

_WS_RE = re.compile(r"\s+")
_NON_WORD_SPACE = re.compile(r"[^\w\s]", flags=re.UNICODE)
_NUM_RE = re.compile(r"\d+", flags=re.UNICODE)

def to_lower(text: str) -> str:
    return text.lower()

def normalize_whitespace(text: str) -> str:
    return " ".join(_WS_RE.split(text))

def strip_punctuation(s: str) -> str:
    s2 = _NON_WORD_SPACE.sub(" ", s)
    return normalize_whitespace(s2)

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


