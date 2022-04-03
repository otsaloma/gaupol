# -*- coding: utf-8-unix -*-

# EDITOR must wait!
EDITOR = nano

check:
	flake8 bin/gaupol
	flake8 aeidon
	flake8 gaupol
	flake8 data/extensions/*/*.py
	flake8 *.py

clean:
	./setup.py clean

install:
	./setup.py install

publish-aeidon:
	$(MAKE) check test clean
	./setup-aeidon.py sdist bdist_wheel
	test -s dist/aeidon-*-py3-none-any.whl
	test -s dist/aeidon-*.tar.gz
	ls -l dist
	printf "Press Enter to upload or Ctrl+C to abort: "; read _
	twine upload dist/*
	sudo pip3 uninstall -y aeidon || true
	sudo pip3 uninstall -y aeidon || true
	sudo pip3 install -U aeidon
	cd && python3 -c "import aeidon; print(aeidon.__file__, aeidon.__version__)"

# Interactive!
release:
	$(MAKE) check test clean
	@echo "BUMP VERSION NUMBERS"
	$(EDITOR) aeidon/__init__.py
	$(EDITOR) gaupol/__init__.py
	$(EDITOR) data/extensions/*/*.in
	@echo "ADD RELEASE NOTES"
	$(EDITOR) NEWS.md
	$(EDITOR) data/io.otsaloma.gaupol.appdata.xml.in
	sudo ./setup.py install --prefix=/usr/local clean
	/usr/local/bin/gaupol
	tools/release
	@echo "REMEMBER TO make publish-aeidon"
	@echo "REMEMBER TO UPDATE FLATPAK"
	@echo "REMEMBER TO UPDATE WEBSITE"

test:
	py.test -xs aeidon gaupol data/extensions

# Interactive!
translations:
	tools/update-translations

warnings:
	python3 -Wd bin/gaupol

.PHONY: check clean install publish-aeidon release test translations warnings
