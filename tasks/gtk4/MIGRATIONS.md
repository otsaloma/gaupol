# Migrations

Migrations from `tasks/gtk4/migrating-3to4.md` that apply to our
codebase, in the order they appear in the guide, titled by the guide's
section headings.

- [x] Stop using `GtkWidget` event signals
- [x] Stop using `gtk_main()` and related APIs
- [x] Stop using GdkScreen
- [x] Adapt to `GdkWindow` API changes
- [x] The "iconified" window state has been renamed to "minimized"
- [x] Adapt to `GdkEvent` API changes
- [x] Replace `GtkClipboard` with `GdkClipboard`
- [x] Adapt to GtkBuilder API changes
- [x] Focus handling changes
- [x] Use the new apis for keyboard shortcuts
- [x] Stop using `GtkEventBox`
- [x] Adapt to `GtkBox` API changes
- [x] Adapt to `GtkWindow` API changes
- [x] Adapt to GtkStack, GtkAssistant and GtkNotebook API changes
- [x] Adapt to GtkContainer removal
- [x] Adapt to gtk_widget_destroy() removal
- [x] Adapt to GtkStyleContext API changes
- [x] Adapt to GtkCssProvider API changes
- [x] Stop using GtkShadowType and GtkRelief properties
- [ ] Adapt to GtkWidget's size request changes
- [ ] Widgets are now visible by default
- [ ] Stop using GtkWidget::draw
- [x] Adapt to cursor API changes
- [ ] Adapt to icon size API changes
- [ ] Adapt to changes in the API of GtkEntry, GtkSearchEntry and GtkSpinButton
- [ ] GtkMenu, GtkMenuBar and GtkMenuItem are gone
- [ ] GtkToolbar has been removed
- [ ] Switch to the new Drag-and-Drop api
- [ ] Adapt to GtkIconTheme API changes
- [ ] Update to GtkFileChooser API changes
- [ ] Stop using blocking dialog functions
- [ ] Adapt to GtkAboutDialog API changes
- [ ] Stop using GtkFileChooserButton

## Removals not covered by the guide

- [ ] `GtkRecentChooserMenu` is gone
- [ ] `GtkTextView` border windows are gone
