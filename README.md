# 常用キット

The Jouyou Kit (`jyk`) is a toolkit for querying information about the
[jouyou kanji](https://en.wikipedia.org/wiki/J%C5%8Dy%C5%8D_kanji).

# Usage

Make calls into the library:

```py
from libjyk import query

query.is_jouyou("猫")
```

# Development

Install the development requirements, and then set up the pre-commit hooks.

```py
pip install -r requirements.dev.txt
pre-commit install
```
