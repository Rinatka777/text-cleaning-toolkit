A tiny, typed, stdlib-only text cleaning toolkit with both a library and a CLI.


Library Usage (Python) Example:

from app.text_cleaner import default_cleaner

cleaner = default_cleaner()
print(cleaner.clean("Hello,   WORLD!!! 123"))   # -> "hello world <NUM>"

CLI Usage Example:

python -m app.cli --text "Hello,   WORLD!!! 123"
-> hello world <NUM>

#from file

python -m app.cli --file ./docs/sample.txt

#With stopwords file

python -m app.cli --file ./docs/sample.txt --stopwords ./docs/stopwords.txt

#Toggles

python -m app.cli --text "Hello, 123" --no-digits
python -m app.cli --text "Hello, 123" --no-punct
python -m app.cli --text "Hello, 123" --no-lower

Design Notes:

-Pure helpers in app/utils/core.py: to_lower, strip_punctuation, replace_digits, normalize_whitespace, remove_stopwords.

-Token-preserving: steps are aware of <NUM>-style placeholders, so cleaning is idempotent.

-OOP wrapper: TextCleaner composes steps; default_cleaner() wires the recommended order.

-CLI: strict argparse contract with mutual exclusion and proper exit codes.