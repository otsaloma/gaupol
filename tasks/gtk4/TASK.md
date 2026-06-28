# Task

We're porting Gaupol from GTK-3 to GTK-4. We need to migrate away from
any classes, functions etc. that have been removed in GTK-4. GTK-4
removes a lot of APIs tied to the X display server, things that are not
supported on Wayland. In such cases, regressions are unavoidable and
acceptable. Otherwise, we try to keep existing functionality, make tests
pass and Gaupol run without errors. GTK-4 brings new deprecations
(things to be removed in GTK-5); of those we'll skip any big and
difficult ones like the `Gtk.TreeView` deprecation.

We don't have a particular version requirement in mind for GTK-4, but as
you migrate pieces, note in the GTK-4 documentation since which GTK-4
version that symbol has been in and we'll set the version requirement to
whatever version justified by having something we need.

## Steps Done

...

## Steps Left

- Review our current unit test coverage. Are we missing some relevant
  tests? Are our tests touching implementation details in a way that the
  tests themselves break too?

- Review the current deprecation warnings we see when running `pytest`
  or `bin/gaupol FILE...`. Let's try to fix these before jumping into
  GTK-4. Fix also any non-GTK, such as Python, deprecation warnings
  while at it.

- Run any automated conversions, such as `gtk4-builder-tool simplify` to
  convert files to whatever new format.

- Switch the codebase to GTK-4 (mainly `gi.require_version` calls in
  `gaupol/__init__.py`). Let's also use this breaking opportunity bump
  versions of all libraries used via `gi.require_version`. We can also
  bump Python version if it comes up for some reason.

- Look through the migration guide to see what we're using that we
  absolutely need to migrate away from. Go through those one-by-one
  switching to whatever new recommended solution.

- Run `pytest` and `bin/gaupol FILE...`, fix any errors you see.

- Apart from errors, there are likely to be warnings caused by new
  deprecations in GTK-4. Let's evaluate these on a case-by-case basis
  and pick some of those to migrate, some to leave for later.

- Finally, review the migration as a whole. Did we migrate something
  only partially? Did we introduce some inconsistencies? Did GTK-4 bring
  something new that would benefit us? Let's consider opportunities to
  simplify or improve the codebase.

## GTK Documentation

GTK documentation is available locally in the following GIR files. Grep
those for any symbols you need.

- `/usr/share/gir-1.0/Gtk-3.0.gir`
- `/usr/share/gir-1.0/Gtk-4.0.gir`

A GTK-3 to GTK-4 migration guide is available in Markdown format.

- `tasks/gtk4/migrating-3to4.md`

Make sure you can access all these documentation in full; abort if not.
Never guess how the API works, always check from the documentation. Keep
in mind that we use Python and some of the documentation has been
written for C. You'll need adapt what you see there, for example:

- `GTK_ALIGN_CENTER` → `Gtk.Align.CENTER`
- `gtk_box_new(...)` → `Gtk.Box(...)`
- `gtk_widget_show(widget)` → `widget.show()`

## Other References

I migrated another GTK app, nfoview, to GTK-4 a while back. See that
codebase under `/home/osmo/Source/nfoview`. The GTK-3 to GTK-4 migration
is commit 256882d16beaa4a353fd498a3a9a159a4fe6f6eb or PR
<https://github.com/otsaloma/nfoview/pull/25>. Make sure you can access
the nfoview code and that migration commit or PR; abort if not. nfoview
is not any gold standard codebase in general, but it's by my hand like
gaupol and thus contains some similar abstractions and conventions and
can be a useful reference.

## Logging

As you progress with the migration work, keep a record as bullet points
in file `tasks/gtk4/LOG.md`. Do not list everything you do, but anything
notable, such changes in behaviour, regressions, tradeoffs, caveats,
things to consider in later parts of the migration etc. Under the
separate "Deferred" section, note any work you left incomplete. That's a
todo-list that must be cleared later.
