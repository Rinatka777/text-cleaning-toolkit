from __future__ import annotations

from collections.abc import Callable
from typing import Optional
from unittest import skipIf

from app.utils import to_lower, normalize_whitespace, strip_punctuation, remove_stopwords, replace_digits
Step = Callable[[str], str]

class TextCleaner:
    def __init__(self, steps: list[Step] | None = None, stopwords: set[str] | None = None):
        self.stopwords = None
        copy_list = steps.copy()
        stopwords = set(stopwords)

    def add_step(self, step: Step) -> None:
        #no idea what to do here

    def clean(self, text: str) -> str:
        for st in step:
            if step == remove_stopwords and self.stopwords is None:
                continue
            else:
                text = step(text)
            return text

    def default_cleaner(stopwords: set[str] | None = None) -> TextCleaner:
        cleaner = TextCleaner(stopwords=stopwords)
        cleaner.add_step(to_lower)
        cleaner.add_step(strip_punctuation)
        cleaner.add_step(replace_digits)
        cleaner.add_step(normalize_whitespace)
        return cleaner
        #stopped at add a wrapper step that captures the set and calls remove_stopwords(s, stopwords)
