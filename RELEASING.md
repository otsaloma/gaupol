Releasing a New Version
=======================

```bash
# Update translations.
tools/update-translations
msgmerge -UN po/fi.po po/gaupol.pot
emacs po/fi.po
tx push -s
tx push -tf -l fi
tx pull -a --minimum-perc=75
tools/check-translations
tools/check-translations | grep %
git commit -a -m "Update translations"

# Check, test, do final edits and release.
python3 -Wd bin/gaupol
pyflakes bin/gaupol aeidon gaupol data/extensions/*/*.py *.py
py.test --tb=no aeidon gaupol data/extensions
emacs */__init__.py data/extensions/*/*.in win32/gaupol.iss
emacs NEWS.md TODO.md
sudo ./setup.py install --prefix=/usr/local clean
/usr/local/bin/gaupol
tools/release

# Build Windows installer (see win32/RELEASING.md).
# Add release notes and Windows installer on GitHub.
# Update web site: <https://otsaloma.io/gaupol/>.
```
