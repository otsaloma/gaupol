# Packaging

This file is for Linux distro packagers. Individual users installing
Gaupol from source, see [`README.md`](README.md) instead.

Gaupol consists of two Python packages: `gaupol`, the GTK user
interface, and `aeidon`, the user interface independent part, which can
be packaged separately. In terms of packaging, you have two options:

1. Build two packages: aeidon and gaupol, where aeidon is a Python
   package installed to site-packages and gaupol is the private-package
   application installed typically to `/usr/share/gaupol`.

2. Build just one package called gaupol. Both aeidon and gaupol install
   as private packages, typically under `/usr/share/gaupol`.

Of these option 1 is recommended for distros to make aeidon available
for other applications that use it. Option 2 is recommended for
individual users and it's what the commands in `README.md` produce.

## Gaupol

    make DESTDIR=/path/to/pkgroot PREFIX=/usr build
    make DESTDIR=/path/to/pkgroot PREFIX=/usr install

Build dependencies: make, coreutils, gettext. Runtime dependencies are
listed in `README.md`.

Paths are patched into files at build time, so `build` and `install`
must be run with the same variables. `make build && make DESTDIR=...
PREFIX=... install` does not work.

Available Make variables:

- `DESTDIR`: prepended to paths at install time only (default empty)
- `PREFIX`: base of all below directories (default `/usr/local`)
- `BINDIR`: launch script (default `$(PREFIX)/bin`)
- `DATADIR`: icons, desktop file, appdata (default `$(PREFIX)/share`)
- `LIBDIR`: Python packages (default `$(DATADIR)/gaupol`)
- `LOCALEDIR`: translations (default `$(DATADIR)/locale`)
- `MANDIR`: man page (default `$(DATADIR)/man`)
- `INCLUDE_AEIDON`: set to `no` to leave out aeidon (default `yes`)

The Python packages are installed privately under `$(LIBDIR)`, not to
site-packages. The launcher adds that directory to `sys.path`.

## Aeidon

`make INCLUDE_AEIDON=no build install` installs gaupol only and the
launcher then imports aeidon from site-packages. Build that aeidon from
`pyproject.toml` (below) and have gaupol depend on the same version.

Of the dependencies listed in `README.md`, iso-codes and
charset-normalizer belong to aeidon, the rest to gaupol.

A standard PEP 517 build from `pyproject.toml`, e.g.

    python3 -m build --no-isolation

Build dependencies: python3-build (or another PEP 517 front-end) and
hatchling ≥1.27.

aeidon bundles copies of iso-codes JSON files under
`aeidon/data/iso-codes`, used at runtime only if `/usr/share/iso-codes`
is missing. To avoid duplicate files, remove that directory before
building and make the package depend on iso-codes.
