Translating Gaupol
==================

Translations are available at [Transifex][1]. Please use that to add and
update translations.

To try your translation, get the gaupol source code from [GitHub][2],
download the translation from Transifex, place it in the `po` directory
and compile that translation to the `locale` directory (which does not
exist by default).

```bash
mkdir -p locale/xx/LC_MESSAGES
msgfmt -cv po/xx.po -o locale/xx/LC_MESSAGES/gaupol.mo
LANG=xx bin/gaupol
```

[1]: https://www.transifex.com/otsaloma/gaupol/
[2]: https://github.com/otsaloma/gaupol
