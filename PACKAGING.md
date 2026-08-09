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

Option 1 is recommended for distros to make aeidon available for other
applications that use it. Option 2 is recommended for individual users
and it's what the commands in `README.md` produce.

## Gaupol

    make build
    make DESTDIR=/path/to/pkg PREFIX=/usr install

Build dependencies: make, coreutils, gettext. Runtime dependencies are
listed in `README.md`. On *BSD, use gmake if you encounter issues.

All Make variables are install-time only, `build` takes none and
produces the same output regardless of where you install it. The two
targets can also be given in one command: `make DESTDIR=... PREFIX=...
build install`.

In addition to `DESTDIR` and `PREFIX`, you might want to use
`INCLUDE_AEIDON=no` to leave out aeidon. See top of the `Makefile` for
all variables you can set.

The Python packages are installed privately under `LIBDIR`, not to
site-packages. The launcher adds that directory to `sys.path`.

## Aeidon

Using `INCLUDE_AEIDON=no` above installs gaupol only and the launcher
then imports aeidon from site-packages. Build that aeidon from
`pyproject.toml` and have gaupol depend on the same version.

Of the dependencies listed in `README.md`, iso-codes and
charset-normalizer belong to aeidon, the rest to gaupol.

A standard PEP 517 build from `pyproject.toml`, e.g.

    python3 -m build --no-isolation

Build dependencies: python3-build (or another PEP 517 front-end) and
hatchling ≥1.27.

aeidon bundles copies of iso-codes JSON files under
`aeidon/data/iso-codes`, used at runtime only if not found under
`/usr/share/iso-codes`. To avoid duplicate files, remove that directory
before building and make the package depend on iso-codes.
