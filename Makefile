# -*- coding: utf-8-unix -*-

# Installation directories without DESTDIR.
# Only used by install, build uses no variables at all.
PREFIX    = /usr/local
BINDIR    = $(PREFIX)/bin
DATADIR   = $(PREFIX)/share
LIBDIR    = $(DATADIR)/gaupol
LOCALEDIR = $(DATADIR)/locale
MANDIR    = $(DATADIR)/man

# Set to 'no' to install gaupol only and have
# the launcher import aeidon from site-packages.
INCLUDE_AEIDON = yes

# EDITOR must wait!
EDITOR = nano

build:
	@echo "BUILDING PYTHON PACKAGES..."
	rm -rf build
	mkdir -p build
	cp -R aeidon gaupol build
	find build -type d -name __pycache__ -prune -exec rm -rf {} +
	find build -type d -name test -prune -exec rm -rf {} +
	@echo "BUILDING TRANSLATIONS..."
	rm -f po/LINGUAS
	ls po/*.po | cut -d/ -f2 | cut -d. -f1 > po/LINGUAS
	mkdir -p build/mo
	for LOCALE in `cat po/LINGUAS`; do msgfmt po/$$LOCALE.po -o build/mo/$$LOCALE.mo; done
	@echo "BUILDING DESKTOP FILE..."
	msgfmt --desktop -d po \
	--template data/io.otsaloma.gaupol.desktop.in \
	-o build/io.otsaloma.gaupol.desktop
	@echo "BUILDING APPDATA FILE..."
	msgfmt --xml -d po \
	--template data/io.otsaloma.gaupol.appdata.xml.in \
	-o build/io.otsaloma.gaupol.appdata.xml
	touch build/.complete

check:
	flake8 bin/gaupol
	flake8 bin/gaupol.in
	flake8 aeidon
	flake8 gaupol
	flake8 *.py
	validate-pyproject pyproject.toml
	for X in gaupol/data/ui/*.ui; do echo $$X; gtk4-builder-tool validate $$X; done

clean:
	rm -rf build
	rm -rf dist
	rm -rf flatpak/.flatpak-builder
	rm -rf flatpak/build
	rm -f po/LINGUAS
	rm -f po/*~
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +

install:
	test -f build/.complete
	@echo "INSTALLING PYTHON PACKAGES..."
	mkdir -p $(DESTDIR)$(LIBDIR)
	test "$(INCLUDE_AEIDON)" = no || cp -R build/aeidon $(DESTDIR)$(LIBDIR)
	cp -R build/gaupol $(DESTDIR)$(LIBDIR)
	sed "s|^LOCALE_DIR = .*$$|LOCALE_DIR = Path('$(LOCALEDIR)')|" build/gaupol/paths.py > $(DESTDIR)$(LIBDIR)/gaupol/paths.py
	grep -qF "$(LOCALEDIR)" $(DESTDIR)$(LIBDIR)/gaupol/paths.py
	@echo "INSTALLING LAUNCHER..."
	mkdir -p $(DESTDIR)$(BINDIR)
	sed "s|%LIBDIR%|$(LIBDIR)|" bin/gaupol.in > $(DESTDIR)$(BINDIR)/gaupol
	grep -qF "$(LIBDIR)" $(DESTDIR)$(BINDIR)/gaupol
	chmod +x $(DESTDIR)$(BINDIR)/gaupol
	@echo "INSTALLING ICONS..."
	mkdir -p $(DESTDIR)$(DATADIR)/icons/hicolor/scalable/apps
	mkdir -p $(DESTDIR)$(DATADIR)/icons/hicolor/symbolic/apps
	cp -f data/io.otsaloma.gaupol.svg $(DESTDIR)$(DATADIR)/icons/hicolor/scalable/apps
	cp -f data/io.otsaloma.gaupol-symbolic.svg $(DESTDIR)$(DATADIR)/icons/hicolor/symbolic/apps
	@echo "INSTALLING TRANSLATIONS..."
	for MO in build/mo/*.mo; do \
	LOCALE=`basename $$MO .mo`; \
	mkdir -p $(DESTDIR)$(LOCALEDIR)/$$LOCALE/LC_MESSAGES; \
	cp -f $$MO $(DESTDIR)$(LOCALEDIR)/$$LOCALE/LC_MESSAGES/gaupol.mo; \
	done
	@echo "INSTALLING DESKTOP FILE..."
	mkdir -p $(DESTDIR)$(DATADIR)/applications
	cp -f build/io.otsaloma.gaupol.desktop $(DESTDIR)$(DATADIR)/applications
	@echo "INSTALLING APPDATA FILE..."
	mkdir -p $(DESTDIR)$(DATADIR)/metainfo
	cp -f build/io.otsaloma.gaupol.appdata.xml $(DESTDIR)$(DATADIR)/metainfo
	@echo "INSTALLING MAN PAGE..."
	mkdir -p $(DESTDIR)$(MANDIR)/man1
	cp -f data/gaupol.1 $(DESTDIR)$(MANDIR)/man1
	@echo "UPDATING DESKTOP DATABASE..."
	test -z "$(DESTDIR)" && update-desktop-database "$(DATADIR)/applications" || true

publish-aeidon:
	$(MAKE) clean
	python3 -m build
	test -s dist/aeidon-*-py3-none-any.whl
	test -s dist/aeidon-*.tar.gz
	twine check dist/*
	ls -l dist
	printf "Press Enter to upload or Ctrl+C to abort: "; read _
	twine upload dist/*

# Interactive!
release:
	$(MAKE) check test clean
	@echo "BUMP VERSION NUMBERS"
	$(EDITOR) aeidon/__init__.py
	$(EDITOR) gaupol/__init__.py
	@echo "ADD RELEASE NOTES"
	$(EDITOR) NEWS.md
	$(EDITOR) data/io.otsaloma.gaupol.appdata.xml.in
	appstream-util validate-relax --nonet data/io.otsaloma.gaupol.appdata.xml.in
	sudo $(MAKE) build install clean
	/usr/local/bin/gaupol
	tools/release
	@echo "REMEMBER TO make publish-aeidon"
	@echo "REMEMBER TO UPDATE FLATPAK"
	@echo "REMEMBER TO UPDATE WEBSITE"

test:
	pytest -xs aeidon gaupol

# Interactive!
translations:
	tools/update-translations

warnings:
	python3 -Wd bin/gaupol

.PHONY: build check clean install publish-aeidon release test translations warnings
