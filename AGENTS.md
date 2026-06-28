# AGENTS.md

## Environment

See `README.md` for which versions of Python, GTK, etc. we're currently
targeting. Regarding operating systems, we currently target only Linux,
but try to avoid any OS-specific code. On Linux, we want to support all
relevant desktops and display servers, but GNOME + Wayland is whose
conventions we want to follow closest.

## Architecture

We have two packages of Python code: `aeidon` and `gaupol`. `aeidon` is
the user-interface independent part and `gaupol` is the GTK application
user interface. The split into two packages was an afterthought and the
separation is not perfect. In all changes, consider this separation and
try to find the right place for any new code.

## Subtitle File Formats

We support many subtitle file formats and want to keep it that way.
However, in practice, SubRip is by far the most common and the most
important. SubRip is the format that needs to work well and other
formats are fine to be just partially supported.

## Extensions

We have an extension system in the `gaupol` package and one extension
`data/extensions/custom-framerates`. The extension system was an
over-engineering mistake and should not be expanded. We'll keep the
system as-is while it doesn't cause any problems.

## Installation Mechanism

Our installation mechanism uses `setup.py` and `setuptools` (formerly
`distutils`). This is deprecated in the Python ecosystem, outdated and
excessively complicated. Avoid making any changes to the installation
mechanism because that causes problems downstream. We'll make breaking
changes in one go at a suitable time later.

## Validation, Testing

After making changes to Python code, always at minimum run `flake8 ...`
and `pytest ...` against all changed files. After bigger changes, or if
you suspect your changes affect other modules, use `make check` and
`make test` to run the full validation and test suites.
