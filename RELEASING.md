Releasing a New Version
=======================

```bash
# Update translations.
tools/update-translations
msgmerge -UN po/fi.po po/gaupol.pot
emacs po/fi.po
tx push -s
tx push -tf --no-interactive -l fi
tx pull -a --minimum-perc=50
sed -i "s/charset=CHARSET/charset=UTF-8/" po/*.po
tools/check-translations
tools/check-translations | grep %
git add po/*.po po/*.pot; git status
git commit -m "Update translations"

# Check, test, do final edits and release.
python3 -Wd bin/gaupol
flake8 bin/gaupol aeidon gaupol data/extensions/*/*.py *.py
py.test --tb=no aeidon gaupol data/extensions
emacs */__init__.py data/extensions/*/*.in win32/gaupol.iss
emacs NEWS.md TODO.md data/io.otsaloma.gaupol.appdata.xml.in
sudo ./setup.py install --prefix=/usr/local clean
/usr/local/bin/gaupol
tools/release
tools/publish-aeidon

# Update Flatpak, website.
# https://github.com/flathub/io.otsaloma.gaupol
# https://github.com/otsaloma/gaupol-www
```
