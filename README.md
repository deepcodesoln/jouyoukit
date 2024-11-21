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

## Development

Dependencies: none.

Tests: none.

## License

[MIT License](./LICENSE.md).
