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
   single command to run at a shell, such as `sudo make build install`
   (although fine to split as `make build` + `sudo make install` to
   avoid root-owned files under the build dir). Any needed installation
   time dependencies should be kept to an absolute minimum.

2. Packaging by Linux distros. This should be a combination of
   "destdir" + "prefix", so installed to a temporary local directory
   with full paths inside and that is then packaged, such as DEB or RPM.
   Many distros package aeidon and gaupol separately, see
   `README.aeidon.md` for how that currently works.

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

`LOCALE_DIR` moves from aeidon to gaupol for the same reason, and
because it has to: it is used only as the default argument of
`aeidon.i18n.bind`, which is called only from `gaupol/__init__.py`, and
in a split install aeidon comes from the wheel and is never touched by
our Makefile, so a patched value there wouldn't exist. gaupol calls
`aeidon.i18n.bind(gaupol.LOCALE_DIR)` instead.

Left in `data/`: files installed to standard system locations — icons,
desktop file, appdata, man page — plus samples and anything else not
read by the app at runtime.

### App Installation (Use Cases 1 and 2)

A catapult-style Makefile using only mkdir/cp/sed/msgfmt:

- `make build` compiles translations (mo files, desktop, appdata),
  generates the launcher from a `bin/gaupol.in` template (sed
  `%LIBDIR%`) and patches `LOCALE_DIR` into a build copy of the paths
  module — everything into `build/`.

  Directory variables are DESTDIR-free and name final paths (`LOCALEDIR
  = $(PREFIX)/share/locale`), with `$(DESTDIR)` prepended only at the
  install sites (`$(DESTDIR)$(LOCALEDIR)`). That's the GNU coding
  standards convention packagers expect, it's what gets patched into
  files as-is, and it avoids both setup.py's abspath-stripping hack and
  catapult's `LOCALEDIR`/`LOCALEDIR_FINAL` pair, where overriding only
  one of the two would silently embed the default path. Same treatment
  for `BINDIR`, `DATADIR` and `MANDIR`, and for the `%LIBDIR%` value
  patched into the launcher.

  Note that paths are embedded at build time, so build and install must
  be run with the same variables — `make LOCALEDIR=... build install`,
  not `make build && make LOCALEDIR=... install`. Document this in
  `PACKAGING.md`.

  `LOCALEDIR` is overridable like `MANDIR`: there is no spec placing
  gettext catalogs at `$PREFIX/share/locale`, only the GNU gettext
  default and FHS convention, so a distro with a house rule must be able
  to say `make LOCALEDIR=... build install`. This is why the path is
  patched in rather than derived at runtime from the package location,
  which would silently fall back to untranslated whenever the two
  disagree.

- `make install` copies the aeidon and gaupol package trees to
  `$(DESTDIR)$(PREFIX)/share/gaupol/`, the launcher to bin, icons,
  desktop, appdata and locale files to their standard directories and
  the man page to `$(MANDIR)` (default `share/man`, overridable — kept
  for NetBSD). As a last best-effort step, run update-desktop-database
  when DESTDIR is unset (distro triggers handle it for `/usr`; without
  it a `/usr/local` install has no mimeinfo.cache and Gaupol wouldn't
  show under "Open With" for subtitle files). No icon cache step: GTK
  scans the theme directory when no cache file exists.

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

There is deliberately no Make variable for the bundled iso-codes JSON
fallback. Stripping those is only a concern for rigorous packagers, who
are the ones doing the split above anyway, and it happens in the aeidon
package they build — leaving one way to do it instead of a different one
for an aeidon-only install and for the full app.

### aeidon on PyPI (Use Case 3)

A minimal pyproject.toml with hatchling as the build backend, dynamic
version from `aeidon/__init__.py`, dependency on charset-normalizer.
With data files inside the package, they are ordinary package data and
the copytree hack dies with `setup-aeidon-pypi.py`. The iso-codes JSON
files ship in the wheel (fixes today's omission; needed on Windows and
Mac where `/usr/share/iso-codes` doesn't exist). Built with `python3 -m
build`, uploaded with twine via `make publish-aeidon`.

No build hooks are needed and nothing but the package itself goes into
the sdist, since pattern files are translated at runtime (see below) and
everything in the wheel is plain package data.

Distros building python3-aeidon that don't want the bundled iso-codes
JSONs strip `aeidon/data/iso-codes` when packaging, this being the only
place where that's done. A per-build option in pyproject.toml isn't
possible anyway, since the file is static config and hatchling doesn't
forward PEP 517 `--config-setting` to build hooks (pypa/hatch#1072).
Document this in `PACKAGING.md`.

The PyPI long description is plain `readme = "README.aeidon.md"` in
pyproject.toml — static config, no dynamic metadata, content type
inferred from the `.md` suffix. Rendering can be checked with `twine
check dist/*`.

### Pattern File Translations

Pattern files stay English-only and are translated at runtime from the
"gaupol" gettext domain instead of having translations merged in at
build time with msgfmt. We don't need to follow desktop file conventions
here, these files are ours alone.

`aeidon.i18n._` already uses the "gaupol" domain and defaults to
`NullTranslations`, so standalone aeidon simply returns the English
strings — which is what we decided we want. Extraction is unaffected:
`tools/extract-translations` keeps reading the pattern files with
`--language=Desktop --keyword=Name --keyword=Description`, the msgids
are the same English strings as before and existing translations in the
po files stay valid.

This removes, in addition to the build steps:

- The `.in` extension and template nature of the pattern files, which
  are renamed to plain `Latn-en.hearing-impaired` etc., and with that
  the logic in `_read_patterns_from_directory` that prefers a translated
  file over an `.in` file when both exist.

- `MetadataItem._get_localized_field` and the `Name[xx_YY@Zzzz]`
  fallback chain it implements. `get_name` and `get_description` run the
  field through gettext instead. `MetadataItem` has no other users
  besides `Pattern`.

Two details to get right:

- `gettext` translates the empty string to the mo file's header
  metadata, so translate only non-empty strings.

- `_filter_patterns` compares an unlocalized `get_name(False)` against a
  localized `get_name()`, so the `Replace` policy silently never matches
  under a non-English locale. This is an existing bug, but worth fixing
  here since we're rewriting the surrounding code; both should be
  unlocalized, the English name being the identifier.

A minor break: local user pattern files with hand-written `Name[xx]`
lines lose those translations. Acceptable for 2.0.

### Removals and Updates

`setup.py`, `setup-aeidon-pypi.py` and `manifests/` are deleted; the
clean target becomes plain shell commands in the Makefile. The CI
workflow (`.github/workflows/test.yml`) is updated to the new commands.

### Documentation

The installation documentation is split by audience:

- `README.md` covers use case 1 only: installation by individuals from
  source, i.e. `sudo make build install`. The current `setup.py` command
  and the `python3-setuptools` dependency go away and make is listed
  instead. It points to `PACKAGING.md` for the other use cases.

- `README.aeidon.md` stays, but only as a description of what aeidon is,
  which is also what the aeidon PyPI page shows. Its content is replaced
  with a Markdown version of the `aeidon` package docstring in
  `aeidon/__init__.py` (the intro and the two usage examples, lines
  19–41), i.e. duplicated by hand and no longer packaging docs. Nothing
  of the old content is worth keeping.

- `PACKAGING.md` is a new file covering use cases 2 and 3: distro
  packaging of gaupol (DESTDIR + PREFIX, the `INCLUDE_AEIDON=no` toggle,
  which dependencies belong to which package) and building aeidon from
  pyproject.toml, including that distros wanting to drop the bundled
  iso-codes JSONs strip `aeidon/data/iso-codes`.

## Progress

The below items are to be done one-by-one, one commit per item.

This work happens on a branch that is only merged once all the items are
done, so files that are going to be deleted along the way — `setup.py`,
`setup-aeidon-pypi.py` and `manifests/` — are not kept up to date with
the intermediate steps.

- [x] Move aeidon data files (headers, patterns, iso-codes) into
      `aeidon/data/`, revise `aeidon/paths.py` to find them relative to
      `__file__`
- [x] Move gaupol data files (ui, gaupol.css) into `gaupol/data/`, add a
      gaupol-side data dir constant, update references; move
      `LOCALE_DIR` to gaupol and pass it to `aeidon.i18n.bind`
- [x] Write the new Makefile build and install targets and the
      `bin/gaupol.in` launcher template; delete `setup.py` and
      `manifests/`
- [x] Translate pattern files at runtime from the "gaupol" domain: drop
      the `.in` extension, translate in `get_name` and `get_description`
      and remove `_get_localized_field`, fix the `_filter_patterns`
      localized/unlocalized comparison, update
      `tools/extract-translations`
- [ ] Add `pyproject.toml` for aeidon, delete `setup-aeidon-pypi.py`,
      update the publish-aeidon target
- [ ] Add a startup warning to stderr if the aeidon and gaupol versions
      differ
- [ ] Update `README.md` to cover use case 1 with the new commands and
      point to `PACKAGING.md`; rewrite `README.aeidon.md` as just a
      description of aeidon; add `PACKAGING.md` covering use cases 2 and
      3
- [ ] Update the CI workflow
- [ ] Verify all three use cases: install to a scratch prefix and run,
      DESTDIR + PREFIX install and inspect paths, build wheel and
      install into a venv and import. Write a permanent test shell
      script `tools/test-install` that tests the different install
      cases, checks that files are in place (`test -f`, `test -x` etc.)
      and that the correct packages are imported, such as
      `PYTHONPATH=... python3 -c ...`

## Out of Scope

- `flatpak/io.otsaloma.gaupol.yml` (updated separately later)

## Open Questions

None at the moment.

## Resolved Questions

- The `--mandir` option existed for non-standard man page locations.
  Keep a MANDIR variable or hardcode `share/man`? => This was requested
  by NetBSD, if I remember correctly, so keep it.

- Post-install hooks: setup.py runs update-desktop-database for
  non-destdir installs. Keep as a best-effort step in `make install`
  (skipped when DESTDIR is set)? Also icon cache? => Keep
  update-desktop-database as a best-effort step in `make install`,
  skipped when DESTDIR is set (distro triggers handle it for `/usr`).
  Without it a `/usr/local` install has no mimeinfo.cache and Gaupol
  wouldn't show under "Open With" for subtitle files. No icon cache step
  needed: GTK scans the theme directory when no cache file exists.

- Windows/frozen leftovers: `sys.platform == "win32"` and `sys.frozen`
  branches in `aeidon/paths.py` and elsewhere — drop them in 2.0 now
  that we target only Linux? => Keep these in case we get back to
  creating Windows installers.

- iso-codes: the bundled JSON files are a fallback when
  `/usr/share/iso-codes` is absent. Keep a `INCLUDE_ISO_CODES=no`
  Makefile toggle for distros? Should the PyPI wheel include them (today
  it doesn't)? => Yeah, we need that toggle. Distros don't want
  duplicate files in packages (they are crazy strict about that). The
  aeidon package does need them, seems a bug in the current packaging.
  Imagine someone on Windows or Mac installing the aeidon package; it
  needs to work. => Refined: no Make variable after all. Only rigorous
  packagers care, they do the split aeidon + gaupol anyway, and we don't
  want one way to strip iso-codes in an aeidon-only install and another
  in the full app. Stripping happens only when building the aeidon
  package.

- `LOCALE_DIR`: sed-patch to `PREFIX/share/locale` at build time
  (catapult-style, standard location), or install app-private under
  `PREFIX/share/gaupol/locale` and find it relative to `__file__` with
  no patching at all? => App-private locale is a strong no-no. We need
  to follow distro conventions, so tools like Debian's localepurge work.
  `PREFIX/share/locale` is correct and that should in 99% of cases be
  `/usr/share/locale` or `/usr/local/share/locale`.

- Translations for standalone aeidon: aeidon strings live in the gaupol
  gettext domain and the wheel ships no mo files, so PyPI users get
  untranslated messages. Accept as status quo? => A stand-alone aeidon
  is used as a package in a way that the strings don't surface to the
  user and no translations are needed. As a package, aeidon is mostly
  just used to read and write subtitle files. The translatable strings
  are defined in aeidon, but only needed for the gaupol GUI, so it's
  fine to use the "gaupol" gettext domain, i.e. only have translations
  if gaupol too is installed.

- Version coupling: when aeidon and gaupol are packaged separately,
  matching versions are assumed. Leave to distro dependency declarations
  as now, or should gaupol check at startup? => Let's add a check, but
  only a warning to stderr, no hard fail.

- Pattern file translation: pattern names and descriptions are
  translated at build time with msgfmt from the `.in` files. Where do
  the generated translated files go in the new layout (`build/` only, or
  generated into `aeidon/data/patterns/`)? And what should the
  standalone aeidon wheel ship — today PyPI effectively gets
  untranslated patterns; options include running msgfmt in a hatchling
  build hook (adds gettext to wheel builds), shipping untranslated, or
  translating at runtime via gettext. => Superseded: keep the files
  English-only and translate at runtime from the "gaupol" domain. We
  don't need to follow desktop file conventions here. This drops the
  build step entirely, in both the Makefile and pyproject.toml, so no
  build hook is needed at all.
