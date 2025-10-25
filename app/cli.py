import argparse
import pathlib
import sys

from app.text_cleaner import TextCleaner
from app.utils import to_lower, strip_punctuation, replace_digits, normalize_whitespace, remove_stopwords

def _load_stopwords(path:Path) -> set[str]:
    with open(path, "r") as file:
        lines = []
        for line in file:
            stripped = line.strip()
            if stripped:
                lines.append(stripped)
        return set(lines)

def _build_cleaner(no_lower: bool, no_punct: bool, no_digits: bool, stopwords: set[str] | None) -> TextCleaner:
    c = TextCleaner()
    if not no_lower:
        c.add_step(to_lower)
    if not no_punct:
        c.add_step(strip_punctuation)
    if not no_digits:
        c.add_step(replace_digits)
    if stopwords is not None:
        c.add_step(lambda s: remove_stopwords(s, stopwords))
    return c

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog = "text-cleaning")
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
            parser.error("file does not exist")
        text = path.read_text(encoding="utf-8", errors="strict")
    else:
        text = args.text

    sw: set[str] | None = None
    if args.stopwords is not None:
        sw_path = Path(args.stopwords)
        if not sw_path.is_file():
            parser.error("stopwords file does not exist")
        sw = _load_stopwords(sw_path)

    cleaner = _build_cleaner(args.no_lower, args.no_punct, args.no_digits, sw)
    out = cleaner.clean(text)
    print(out)
    return 0

if __name__ == "__main__":
    sys.exit(main())




