# 常用キット

The Jouyou Kit (`jyk`) is a toolkit for querying information about the
[jouyou kanji](https://en.wikipedia.org/wiki/J%C5%8Dy%C5%8D_kanji).

# Usage

This library requires Python 3.9 or newer.

Make calls into the library:

```py
from libjyk import query

query.is_jouyou("猫")
```

Use the CLI:

```
python3 jyk.py -h

python3 jyk.py db --build path/to/kanjidic2.xml
python3 jyk.py db --query-kanji 猫
```

# Development

Install the development requirements, and then set up the pre-commit hooks.

```
pip install -r requirements.dev.txt
pre-commit install
```

## Running Tests

Run `pytest` as a module to make sure you use the correct Python version.

```
python3 -m pytest tests
```

# License

[MIT license](./LICENSE.md).
