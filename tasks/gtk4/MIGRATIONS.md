# Migrations

Migrations from `tasks/gtk4/migrating-3to4.md` that apply to our
codebase, in the order they appear in the guide, titled by the guide's
section headings.

- [ ] Stop using `GtkWidget` event signals
- [ ] Stop using `gtk_main()` and related APIs
- [ ] Stop using GdkScreen
- [ ] Adapt to `GdkWindow` API changes
- [ ] The "iconified" window state has been renamed to "minimized"
- [ ] Adapt to `GdkEvent` API changes
- [ ] Replace `GtkClipboard` with `GdkClipboard`
- [ ] Adapt to GtkBuilder API changes
- [ ] Focus handling changes
- [ ] Use the new apis for keyboard shortcuts
- [ ] Stop using `GtkEventBox`
- [ ] Adapt to `GtkBox` API changes
- [ ] Adapt to `GtkWindow` API changes
- [ ] Adapt to GtkStack, GtkAssistant and GtkNotebook API changes
- [ ] Adapt to GtkContainer removal
- [ ] Adapt to gtk_widget_destroy() removal
- [ ] Adapt to GtkStyleContext API changes
- [ ] Adapt to GtkCssProvider API changes
- [ ] Stop using GtkShadowType and GtkRelief properties
- [ ] Adapt to GtkWidget's size request changes
- [ ] Widgets are now visible by default
- [ ] Stop using GtkWidget::draw
- [ ] Adapt to cursor API changes
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
