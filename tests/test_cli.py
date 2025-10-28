from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _run_cli(*args: str) -> tuple[int, str, str]:
    cmd = [sys.executable, "-m", "app.cli", *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def test_requires_one_input() -> None:
    rc, _out, _err = _run_cli()
    assert rc == 2


def test_mutual_exclusion() -> None:
    rc, _out, _err = _run_cli("--text", "x", "--file", "y.txt")
    assert rc == 2


def test_text_happy() -> None:
    rc, out, _err = _run_cli("--text", "Hello,   WORLD!!! 123")
    assert rc == 0
    assert out.strip() == "hello world <NUM>"


def test_file_happy(tmp_path: Path) -> None:
    p = tmp_path / "in.txt"
    p.write_text("Hello,   WORLD!!! 123", encoding="utf-8")
    rc, out, _err = _run_cli("--file", str(p))
    assert rc == 0
    assert out.strip() == "hello world <NUM>"


def test_stopwords_file(tmp_path: Path) -> None:
    p = tmp_path / "in.txt"
    p.write_text("this is a test", encoding="utf-8")
    sw = tmp_path / "sw.txt"
    sw.write_text("is\na\n", encoding="utf-8")
    rc, out, _err = _run_cli("--file", str(p), "--stopwords", str(sw))
    assert rc == 0
    assert out.strip() == "this test"


def test_toggles_no_digits() -> None:
    rc, out, _err = _run_cli("--text", "Hello, 123", "--no-digits")
    assert rc == 0
    # punctuation still stripped, case lowered unless --no-lower set
    assert out.strip() == "hello 123"


def test_toggles_no_punct() -> None:
    rc, out, _err = _run_cli("--text", "Hello, 123", "--no-punct")
    assert rc == 0
    # no punctuation stripping, but whitespace normalized and lowercased
    assert out.strip() == "hello, <NUM>"


def test_toggles_no_lower() -> None:
    rc, out, _err = _run_cli("--text", "Hello, 123", "--no-lower")
    assert rc == 0
    # case preserved
    assert out.strip() == "Hello <NUM>"


def test_missing_file_gives_code_2() -> None:
    rc, _out, _err = _run_cli("--file", "nope.txt")
    assert rc == 2


def test_missing_stopwords_gives_code_2(tmp_path: Path) -> None:
    p = tmp_path / "in.txt"
    p.write_text("this is a test", encoding="utf-8")
    missing_sw = tmp_path / "missing.txt"
    rc, _out, _err = _run_cli("--file", str(p), "--stopwords", str(missing_sw))
    assert rc == 2