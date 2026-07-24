# New Installation Mechanism

We're using a severely outdated installation mechanism in `setup.py`
written originally for distutils and then minimally ported over to
setuptools. Even originally this was probably a mistake, suitable for a
Python package, but not so much for a desktop app. That `setup.py` is
overlong and unclear because we picked the wrong tool to do all those
things that are there. We need to rewrite this entirely to modernize,
clarify and simplify.

## Important Criteria

We have accumulated several different installation uses and all these
need to continue to be supported.

1. Installation by individuals from source. This should install Gaupol
   to a "prefix", `/usr/local` by default. This should ideally be just a
   single command to run at a shell, such as `sudo make build install`.
   Any needed installation time dependencies should be kept to an
   absolute minimum.

2. Packaging by Linux distros. This should be a combination of "root" +
   "prefix", so installed to a temporary local directory with full paths
   inside and that is then packaged, such as DEB or RPM. Many distros
   package aeidon and gaupol separately, see `README.aeidon.md` for how
   that currently works.

3. The aeidon package is published on PyPI and needs to be installable
   and packageable stand-alone (no gaupol, no GUI). This is currently
   done by `setup-aeidon-pypi.py` but that contains some data file hacks
   in addition to using the deprecated setup.py and setuptools.

## References

In more recent years, I've written notably two different installation
mechanisms which reflect my preferences on how these things should be
done.

- A better GUI application installation is available in
  `/home/osmo/Source/catapult/Makefile`. It's basically a private
  package under PREFIX/share/catapult and the Makefile just copies files
  using shell commands. This is the kind of simplicity I'd favor. Make +
  shell commands are simple, have been around since forever, work
  everywhere and will never be deprecated.

- A better Python package installation is available in
  `/home/osmo/Source/dataiter/pyproject.toml` +
  `/home/osmo/Source/dataiter/Makefile`. That pyproject.toml +
  hatchling + pip + build is, while a bit fragmented, a good preference
  here as well since we're not using a full environment like uv
  (although can consider it if it helps).

## Notes

- We have liberty to redesign how data files are accessed. We've done it
  one way for the full app using `aeidon/paths.py` and a hack in
  `setup-aeidon-pypi.py` (which by the way means we probably have a
  conflict if a user has installed both the PyPI package and the full
  app). We can relocate data files in the source tree, we can revise
  path constants, anything that's needed to make this work right.

- Everything else is up for reconsideration and dramatic changes as
  well. This is going to be a breaking change for Linux distro packagers
  and we might as well use this opportunity fix everything at once and
  pile all breaking changes in our next 2.0 release. Then keep things
  stable after that.

## Plan

Two small mechanisms, each idiomatic for its purpose: the app is
installed catapult-style with Make + shell commands as a private
package, and aeidon for PyPI is built with a minimal dataiter-style
pyproject.toml. The overlong setup.py serving neither purpose well is
deleted.

### Data Files

Data files that the packages read at runtime move inside the packages
and are found relative to `__file__`:

- `data/headers` → `aeidon/data/headers`
- `data/iso-codes` → `aeidon/data/iso-codes`
- `data/patterns` → `aeidon/data/patterns`
- `data/ui` → `gaupol/data/ui`
- `data/gaupol.css` → `gaupol/data/gaupol.css`

The same lookup logic then works running from source, installed
privately under a prefix and installed from a wheel — no build-time path
rewriting for data files and no PyPI-vs-app conflict. The single shared
`aeidon.DATA_DIR` is replaced by per-package constants: gaupol gets its
own data dir constant in the gaupol package for its ui and css files,
which also improves the aeidon/gaupol separation.

Left in `data/`: files installed to standard system locations — icons,
desktop file, appdata, man page — plus samples and anything else not
read by the app at runtime.

### App Installation (Use Cases 1 and 2)

A catapult-style Makefile using only mkdir/cp/sed/msgfmt:

- `make build` compiles translations (mo files, desktop, appdata,
  pattern files), generates the launcher from a `bin/gaupol.in` template
  (sed `%LIBDIR%`) and patches `LOCALE_DIR` into a build copy of the
  paths module — everything into `build/`.

- `make install` copies the aeidon and gaupol package trees to
  `$(DESTDIR)$(PREFIX)/share/gaupol/`, the launcher to bin, and icons,
  desktop, appdata, man page and locale files to their standard
  directories.

- Use case 1 is `sudo make build install` (PREFIX=/usr/local by
  default). Use case 2 is `make DESTDIR=... PREFIX=/usr build install`.
  Install-time dependencies: make, coreutils, gettext.

The default install bundles aeidon privately, so nothing global is
touched and no conflicts with a distro or PyPI aeidon are possible. For
distros that split the packages, `make INCLUDE_AEIDON=no install`
installs only the gaupol half and the launcher falls back to importing
aeidon from site-packages, provided by a python3-aeidon distro package
built from the same pyproject.toml as PyPI, using the distro's standard
Python packaging tooling.

### aeidon on PyPI (Use Case 3)

A minimal pyproject.toml with hatchling as the build backend, dynamic
version from `aeidon/__init__.py`, dependency on charset-normalizer.
With data files inside the package, they are ordinary package data and
the copytree hack dies with `setup-aeidon-pypi.py`. Built with `python3
-m build`, uploaded with twine via `make publish-aeidon`.

### Removals and Updates

`setup.py`, `setup-aeidon-pypi.py` and `manifests/` are deleted; the
clean target becomes plain shell commands in the Makefile. The flatpak
manifest, CI workflow (`.github/workflows/test.yml`), `README.md` and
`README.aeidon.md` (rewritten distro-packaging instructions) are updated
to the new commands.

## Progress

- [ ] Move aeidon data files (headers, patterns, iso-codes) into
      `aeidon/data/`, revise `aeidon/paths.py` to find them relative to
      `__file__`
- [ ] Move gaupol data files (ui, gaupol.css) into `gaupol/data/`, add a
      gaupol-side data dir constant, update references
- [ ] Write the new Makefile build and install targets and the
      `bin/gaupol.in` launcher template; delete `setup.py` and
      `manifests/`
- [ ] Add `pyproject.toml` for aeidon, delete `setup-aeidon-pypi.py`,
      update the publish-aeidon target
- [ ] Update `README.md` and `README.aeidon.md` installation and
      packaging instructions
- [ ] Update the CI workflow
- [ ] Verify all three use cases: install to a scratch prefix and run,
      DESTDIR + PREFIX install and inspect paths, build wheel and
      install into a venv and import

## Out of Scope

- `flatpak/io.otsaloma.gaupol.yml` (updated separately later)

## Resolved Questions

...

## Open Questions

- Pattern file translation: pattern names and descriptions are
  translated at build time with msgfmt from the `.in` files. Where do
  the generated translated files go in the new layout (`build/` only, or
  generated into `aeidon/data/patterns/`)? And what should the
  standalone aeidon wheel ship — today PyPI effectively gets
  untranslated patterns; options include running msgfmt in a hatchling
  build hook (adds gettext to wheel builds), shipping untranslated, or
  translating at runtime via gettext.

- iso-codes: the bundled JSON files are a fallback when
  `/usr/share/iso-codes` is absent. Keep a `INCLUDE_ISO_CODES=no`
  Makefile toggle for distros? Should the PyPI wheel include them (today
  it doesn't)?

- Translations for standalone aeidon: aeidon strings live in the gaupol
  gettext domain and the wheel ships no mo files, so PyPI users get
  untranslated messages. Accept as status quo?

- `LOCALE_DIR`: sed-patch to `PREFIX/share/locale` at build time
  (catapult-style, standard location), or install app-private under
  `PREFIX/share/gaupol/locale` and find it relative to `__file__` with
  no patching at all?

- Windows/frozen leftovers: `sys.platform == "win32"` and `sys.frozen`
  branches in `aeidon/paths.py` and elsewhere — drop them in 2.0 now
  that we target only Linux?

- Post-install hooks: setup.py runs update-desktop-database for non-root
  installs. Keep as a best-effort step in `make install` (skipped when
  DESTDIR is set)? Also icon cache?

- The `--mandir` option existed for non-standard man page locations.
  Keep a MANDIR variable or hardcode `share/man`?

- Version coupling: when aeidon and gaupol are packaged separately,
  matching versions are assumed. Leave to distro dependency declarations
  as now, or should gaupol check at startup?
