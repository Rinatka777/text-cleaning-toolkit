import argparse
import pathlib
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




