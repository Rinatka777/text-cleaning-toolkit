from __future__ import annotations

from collections.abc import Callable
from typing import TypeAlias

from app.utils import (
    normalize_whitespace,
    replace_digits,
    strip_punctuation,
    to_lower,
)
from app.utils import (
    remove_stopwords as _remove_stopwords,
)

Step: TypeAlias = Callable[[str], str]


def _make_stop_step(sw: set[str]) -> Step:
    def _step(s: str) -> str:
        return _remove_stopwords(s, sw)
    return _step


class TextCleaner:
    def __init__(self, steps: list[Step] | None = None, stopwords: set[str] | None = None) -> None:
        self.steps: list[Step] = list(steps) if steps is not None else []
        self.stopwords: set[str] | None = stopwords

    def add_step(self, step: Step) -> None:
        self.steps.append(step)

    def clean(self, text: str) -> str:
        out = text
        for step in self.steps:
            out = step(out)
        return out


def default_cleaner(stopwords: set[str] | None = None) -> TextCleaner:
    cleaner = TextCleaner(stopwords=stopwords)
    cleaner.add_step(to_lower)
    cleaner.add_step(strip_punctuation)
    cleaner.add_step(replace_digits)
    cleaner.add_step(normalize_whitespace)
    if stopwords is not None:
        cleaner.add_step(_make_stop_step(stopwords))
    return cleaner


__all__ = ["TextCleaner", "default_cleaner", "Step"]