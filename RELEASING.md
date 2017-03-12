Releasing a New Version
=======================

* Update translations
    - `tools/update-translations`
    - `msgmerge -UN po/fi.po po/gaupol.pot`
    - `emacs po/fi.po`
    - `tx push -s`
    - `tx push -tf -l fi`
    - `tx pull -a --minimum-perc=75`
    - `tools/check-translations`
    - `tools/check-translations | grep %`
    - `git commit -a -m "Update translations for X.Y.Z"`
* Do final quality checks
    - `python3 -Wd bin/gaupol`
    - `pyflakes aeidon gaupol bin/gaupol data/extensions/*/*.py *.py`
    - `py.test --tb=no aeidon`
    - `py.test --tb=no gaupol`
    - `py.test --tb=no data/extensions`
* Bump version numbers
    - `aeidon/__init__.py`
    - `gaupol/__init__.py`
    - `data/extensions/*/*.extension.in`
* Update `NEWS.md` and `TODO.md`
* Check that installation works
    - `sudo python3 setup.py install --prefix=/usr/local`
    - `sudo python3 setup.py clean`
    - `/usr/local/bin/gaupol`
* Commit changes
    - `git commit -a -m "RELEASE X.Y.Z"`
    - `git tag -s X.Y.Z`
    - `git push`
    - `git push --tags`
* Build Windows installer (see [`win32/RELEASING.md`](win32/RELEASING.md))
* Add release notes and Windows installer on GitHub
* Update web sites
    - <http://otsaloma.io/gaupol/>
