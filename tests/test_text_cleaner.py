from __future__ import annotations

import pytest

from app.text_cleaner import Step, TextCleaner, default_cleaner
from app.utils import (
    normalize_whitespace,
    to_lower,
)
from app.utils import (
    remove_stopwords as _remove_stopwords,
)


@pytest.fixture()
def stopwords_set() -> set[str]:
    return {"is", "a", "the"}


def _stop_step_factory(sw: set[str]) -> Step:
    def step(s: str) -> str:
        return _remove_stopwords(s, sw)
    return step


def test_order_matters_lower_vs_stopwords(stopwords_set: set[str]) -> None:
    # lower -> stop -> norm
    c1 = TextCleaner()
    c1.add_step(to_lower)
    c1.add_step(_stop_step_factory(stopwords_set))
    c1.add_step(normalize_whitespace)

    # stop -> lower -> norm
    c2 = TextCleaner()
    c2.add_step(_stop_step_factory(stopwords_set))
    c2.add_step(to_lower)
    c2.add_step(normalize_whitespace)

    text = "IS a Test"
    out1 = c1.clean(text)
    out2 = c2.clean(text)

    assert out1 == "test"
    assert out2 == "is test"
    assert out1 != out2


def test_default_pipeline_basic() -> None:
    cln = default_cleaner(stopwords=None)
    assert cln.clean("Hello,   WORLD!!! 123") == "hello world <NUM>"


def test_stopwords_optional(stopwords_set: set[str]) -> None:
    cln_with = default_cleaner(stopwords_set)
    cln_without = default_cleaner(None)
    assert cln_with.clean("this is a test") == "this test"
    assert cln_without.clean("this is a test") == "this is a test"


def test_idempotency() -> None:
    cln = default_cleaner()
    s = "Hello,   WORLD!!! 123"
    once = cln.clean(s)
    twice = cln.clean(once)
    assert once == twice


def test_unicode_digits() -> None:
    cln = default_cleaner()
    assert cln.clean("Привет,\nмир ١٢٣!") == "привет мир <NUM>"


def test_edges(stopwords_set: set[str]) -> None:
    cln = default_cleaner(stopwords_set)
    assert cln.clean("") == ""
    assert cln.clean(".,!_:;?=)(") == ""


def test_all_stopwords_become_empty() -> None:
    cln = default_cleaner(stopwords={"a", "the"})
    assert cln.clean("the a the") == ""


