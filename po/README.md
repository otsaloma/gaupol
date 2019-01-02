Translating Gaupol
==================

Translations are available at [Transifex][]. Please use that to add and
update translations.

To try your translation, get the source code from GitHub, add your
translation file from Transifex, compile your translation and run.

```bash
git clone https://github.com/otsaloma/gaupol.git
cd gaupol
# Download your translation as po/xx.po.
# https://www.transifex.com/otsaloma/gaupol/language/xx/
mkdir -p locale/xx/LC_MESSAGES
msgfmt -cv po/xx.po -o locale/xx/LC_MESSAGES/gaupol.mo
LANG=xx bin/gaupol
```

[Transifex]: https://www.transifex.com/otsaloma/gaupol/
