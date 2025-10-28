from __future__ import annotations

import argparse
import sys
from pathlib import Path

from app.text_cleaner import TextCleaner
from app.utils import (
    normalize_whitespace,
    remove_stopwords,
    replace_digits,
    strip_punctuation,
    to_lower,
)


def _load_stopwords(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    words: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if s:
            words.append(s)
    return set(words)


def _build_cleaner(
    no_lower: bool,
    no_punct: bool,
    no_digits: bool,
    stopwords_set: set[str] | None,
) -> TextCleaner:
    c = TextCleaner()
    if not no_lower:
        c.add_step(to_lower)
    if not no_punct:
        c.add_step(strip_punctuation)
    if not no_digits:
        c.add_step(replace_digits)
    # Always normalize at the end to collapse whitespace and strip edges.
    c.add_step(normalize_whitespace)
    if stopwords_set is not None:
        # Simple adapter to pass the set into the pure function.
        c.add_step(lambda s: remove_stopwords(s, stopwords_set))
    return c


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="text-cleaning")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str)
    group.add_argument("--file", type=str)
    parser.add_argument("--stopwords", type=str)
    parser.add_argument("--no-digits", action="store_true")
    parser.add_argument("--no-punct", action="store_true")
    parser.add_argument("--no-lower", action="store_true")

    args = parser.parse_args(argv)

    if args.file:
        path = Path(args.file)
        if not path.is_file():
            parser.error("file does not exist")  # exits with code 2
        text = path.read_text(encoding="utf-8", errors="strict")
    else:
        text = args.text

    sw: set[str] | None = None
    if args.stopwords is not None:
        sw_path = Path(args.stopwords)
        if not sw_path.is_file():
            parser.error("stopwords file does not exist")  # exits with code 2
        sw = _load_stopwords(sw_path)

    cleaner = _build_cleaner(args.no_lower, args.no_punct, args.no_digits, sw)
    out = cleaner.clean(text)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())