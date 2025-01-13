# 常用キット (jouyoukit)

jouyoukit is a Python utility that extracts
[jouyou](https://en.wikipedia.org/wiki/J%C5%8Dy%C5%8D_kanji) kanji and related
vocabulary from popular, free Japanese dictionaries.

## Usage

Tested with Python 3.13. You will need the KANJIDIC2 XML database, available
[here](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project), and the JMdict XML
database, available
[here](http://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project).

First, build a local jouyou kanji JSON database and then emit the jouyou kanji
as CSV as shown below.

```
$ python3 jyk.py build_db kanjidic2.xml JMdict_e.xml
$ python3 jyk.py db_to_csv
```

## CSV Schema

A single row contains the following values:

1. kanji character
1. radical and any variants
1. kanji onyomi readings
1. kanji kunyomi readings
1. kanji meanings
1. kanji grade
1. kanji frequency
1. vocabulary 1 term
1. vocabulary 1 readings
1. vocabulary 1 meanings
1. vocabulary 2 term
1. vocabulary 2 readings
1. vocabulary 2 meanings

Some fields may be empty: the onyomi or kunyomi (but not both), the frequency,
and one or both vocabulary terms and their readings and meanings.

## Development

Dependencies: none.

Tests: manually verified with Anki.

## License

[MIT License](./LICENSE.md).
