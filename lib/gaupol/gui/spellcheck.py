# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Spell-checking window."""


from enchant.checker import SpellChecker
import enchant
import os

try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk
import pango

from gaupol.gui.dialogs.error import SpellCheckErrorDialog
from gaupol.gui.util import gui
from gaupol.lib.colcons import TEXT, TRAN
from gaupol.lib.util import langlib


PWL_DIR = os.path.join(os.path.expanduser('~'), '.gaupol', 'pwl')


class TextEditDialog(gtk.Dialog):

    def __init__(self, parent, text):
    
        gtk.Dialog.__init__(self)
        
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_default_response(gtk.RESPONSE_OK)
        
        self.set_has_separator(False)
        self.set_transient_for(parent)
        self.set_border_width(6)
        self.set_modal(True)
        
        # Create TextView.
        self._text_view = gtk.TextView()
        self._text_view.set_wrap_mode(gtk.WRAP_NONE)
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(unicode(text))

        # Put TextView in a scrolled window.
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_border_width(6)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_shadow_type(gtk.SHADOW_IN)
        scrolled_window.add(self._text_view)
        
        width, height = self._text_view.size_request()
        width  = min(400, width  + 24)
        height = min(200, height + 24)
        self._text_view.set_size_request(width, height)
        
        self.get_child().add(scrolled_window)
        self.show_all()
        
    def get_text(self):
    
        text_buffer = self._text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end, True)

class SpellCheckWindow(gobject.GObject):

    """
    Spell-checking window.
    
    All requests to update the application window are sent out as GObject
    signals.
    """
    
    STAGE = gobject.SIGNAL_RUN_LAST
    INT   = gobject.TYPE_INT

    __gsignals__ = {
        'project-selected': (STAGE, None, (object, )        ),
        'cell-selected'   : (STAGE, None, (object, INT, INT)),
        'checking-done'   : (STAGE, None, ()              ),
    }
    
    def __init__(self, parent, projects, check_text, check_tran,
                 text_lang, tran_lang):
                 
        gobject.GObject.__init__(self)
        
        self._row  = 0
        self._col  = None
        self._cols = []
        
        self._projects = projects
        self._project  = projects[0]
        
        self._lang_labels = []
        
        self._checker  = None
        self._checkers = []
        
        self._emph_tag = None
    
        glade_xml = gui.get_glade_xml('spellcheck-window.glade')
        w = glade_xml.get_widget
        
        # Widgets
        self._window             = w('window')
        self._text_view          = w('text_view')
        self._entry              = w('entry')
        self._tree_view          = w('suggestion_tree_view')
        self._edit_button        = w('edit_button')
        self._check_button       = w('check_button')
        self._ignore_button      = w('ignore_button')
        self._ignore_all_button  = w('ignore_all_button')
        self._replace_button     = w('replace_button')
        self._replace_all_button = w('replace_all_button')
        self._add_button         = w('add_button')
        self._add_lower_button   = w('add_lower_button')
        self._language_label     = w('language_label')
        self._close_button       = w('close_button')
        
        self._prepare_gui(glade_xml, parent)
        
        self._window.show()
        
        self._set_checkers(check_text, check_tran, text_lang, tran_lang)
        self._checker.set_text(self._project.data.texts[self._row][self._col])
        self._advance()
        
    def _advance(self):
        """Advance to the next error."""
        
        try:
            self._checker.next()
        except StopIteration:
            text = self._checker.get_text()
            text = unicode(text)
            old_text = self._project.data.texts[self._row][self._col]
            self._project.data.set_text(self._row, self._col, text)
            if text != old_text:
                self._project.reload_data_in_row(self._row)
            try:
                self._get_next_text()
            except IndexError:
                self._on_close_button_clicked()
                return
            self._advance()
            return
            
        self.emit('cell-selected', self._project, self._row, self._col)
        
        buffer = self._text_view.get_buffer()
        buffer.set_text(unicode(self._checker.get_text()))
        
        start = self._checker.wordpos
        end = start + len(self._checker.word)
        start = buffer.get_iter_at_offset(start)
        end = buffer.get_iter_at_offset(end)
        buffer.apply_tag(self._emph_tag, start, end)
        
        suggestions = self._checker.suggest()
        model = self._tree_view.get_model()
        model.clear()
        for suggestion in suggestions:
            model.append([unicode(suggestion)])
        selection = self._tree_view.get_selection()
        if suggestions:
            selection.unselect_all()
            selection.select_path(0)
        
    def _get_checker(self, lang, use_pwl):
        """Get dictionary for lang."""
        
        if use_pwl:
            pwl_path = os.path.join(PWL_DIR, '%s.pwl' % lang)
            try:
                dict = enchant.DictWithPWL(lang, pwl_path)
            except enchant.Error, detail:
                dialog = SpellCheckErrorDialog(self._window, detail)
                dialog.run()
                dialog.destroy()
                self._on_close_button_clicked()
        else:
            try:
                dict = enchant.Dict(lang)
            except enchant.Error, detail:
                dialog = SpellCheckErrorDialog(self._window, detail)
                dialog.run()
                dialog.destroy()
                self._on_close_button_clicked()
                    
        return SpellChecker(dict, u'')
        
    def _get_next_text(self):
        """Get next text unit for checker."""
        
        texts = self._project.data.texts
        
        # Move to next row.
        try:
            text = texts[self._row + 1][self._col]
            self._row += 1
        
        # Move to next column.
        except IndexError:
            try:
                index = self._cols.index(self._col)
                self._col = self._cols[index + 1]
                self._checker = self._checkers[index + 1]
                self._row = 0
                text = texts[self._row][self._col]
            
            # Move to next project.
            except IndexError:
                try:
                    index = self._projects.index(self._project)
                    self._project = self._projects[index + 1]
                    texts = self._project.data.texts
                    text = texts[self._row][self._col]
                    self.emit('project-selected', self._project)
                except IndexError:
                    # TODO: done.
                    raise

        
        self._checker.set_text(text)

    
    
    def _on_add_button_clicked(self, *args):
    
        word = self._checker.word
        self._checker.dict.add_to_pwl(unicode(word))
        self._advance()
    
    def _on_add_lower_button_clicked(self, *args):
    
        word = self._checker.word.lower()
        self._checker.dict.add_to_pwl(unicode(word))
        self._advance()
    
    def _on_check_button_clicked(self, *args):
    
        word = self._entry.get_text()
        suggestions = self._checker.suggest(unicode(word))
        model = self._tree_view.get_model()
        model.clear()
        for suggestion in suggestions:
            model.append([unicode(suggestion)])
        selection = self._tree_view.get_selection()
        if suggestions:
            selection.unselect_all()
            selection.select_path(0)
    
    def _on_close_button_clicked(self, *args):
    
        self._window.destroy()
        self.emit('checking-done')
    
    def _on_edit_button_clicked(self, *args):
    
        text = self._checker.get_text()
        dialog = TextEditDialog(self._window, unicode(text))
        response = dialog.run()
        text = dialog.get_text()
        dialog.destroy()
        
        if response == gtk.RESPONSE_OK:
            self._checker.set_text(unicode(text))
            self._advance()
        
    def _on_ignore_all_button_clicked(self, *args):

        self._checker.ignore_always()
        self._advance()

    def _on_ignore_button_clicked(self, *args):
        """Ignore the current error and move to the next error."""
        
        self._advance()
        
    def _on_replace_button_clicked(self, *args):
    
        word = self._entry.get_text()
        self._checker.replace(unicode(word))
        self._advance()
    
    def _on_replace_all_button_clicked(self, *args):
    
        word = self._entry.get_text()
        self._checker.replace_always(unicode(word))
        self._advance()
    
    def _on_tree_view_selection_changed(self, selection):
    
        model, rows = selection.get_selected_rows()
        
        if not rows:
            self._entry.set_text(u'')
            return
        else:
            row = rows[0]
            
        word = model[row][0]
        self._entry.set_text(unicode(word))
        
    def _on_window_delete_event(self, *args):
    
        self._on_close_button_clicked()
        return True
    
    def _prepare_gui(self, glade_xml, parent):
        """Prepare mnemonics, connect signals and set gui properties."""
        
        # Window
        self._window.set_transient_for(parent)
        self._window.connect('delete_event', self._on_window_delete_event)
        
        # Set mnemonics.
        entry_label = glade_xml.get_widget('entry_label')
        entry_label.set_mnemonic_widget(self._entry)
        suggestion_label = glade_xml.get_widget('suggestion_label')
        suggestion_label.set_mnemonic_widget(self._tree_view)
        
        # Connect button signals.
        signals = [
            (self._edit_button       , self._on_edit_button_clicked       ),
            (self._check_button      , self._on_check_button_clicked      ),
            (self._ignore_button     , self._on_ignore_button_clicked     ),
            (self._ignore_all_button , self._on_ignore_all_button_clicked ),
            (self._replace_button    , self._on_replace_button_clicked    ),
            (self._replace_all_button, self._on_replace_all_button_clicked),
            (self._add_button        , self._on_add_button_clicked        ),
            (self._add_lower_button  , self._on_add_lower_button_clicked  ),
            (self._close_button      , self._on_close_button_clicked      ),
        ]
        
        for button, signal in signals:
            button.connect('clicked', signal)
            
        # Add emphasis tag to text view's tag table.
        text_buffer = self._text_view.get_buffer()
        tag_table = text_buffer.get_tag_table()
        tag = gtk.TextTag()
        tag.set_property('weight', pango.WEIGHT_BOLD)
        tag_table.add(tag)
        
        self._emph_tag = tag
            
        self._prepare_tree_view()
        
    def _prepare_tree_view(self):
        """Prepare the properties of the tree view."""
    
        self._tree_view.columns_autosize()
        
        model = gtk.ListStore(gobject.TYPE_STRING)
        self._tree_view.set_model(model)

        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()
        selection.connect('changed', self._on_tree_view_selection_changed)
        
        cell_renderer = gtk.CellRendererText()
        tree_view_column = gtk.TreeViewColumn('' , cell_renderer, text=0)
        self._tree_view.append_column(tree_view_column)
    
    def _set_checkers(self, check_text, check_tran, text_lang, tran_lang):
        """Set spell-checker objects."""
    
        # Create directory ~/.gaupol/pwl if it doesn't exist.
        use_pwl = True
        if not os.path.isdir(PWL_DIR):
            try:
                os.makedirs(PWL_DIR)
            except OSError, detail:
                use_pwl = False
                logger.error( \
                    'Failed to create personal word list directory "%s": %s.' \
                    % (PWL_DIR, detail) \
                )
                self._add_button.set_sensitive(False)
                self._add_lower_button.set_sensitive(False)
    
        # Add text column spell-checker.
        if check_text:
        
            self._checkers.append(self._get_checker(text_lang, use_pwl))
            self._cols.append(TEXT)
            self._lang_labels.append(langlib.get_descriptive_name(text_lang))
        
        # Add translation column spell-checker.
        if check_tran:
        
            self._checkers.append(self._get_checker(tran_lang, use_pwl))
            self._cols.append(TRAN)
            self._lang_labels.append(langlib.get_descriptive_name(tran_lang))
            
        self._col = self._cols[0]
        self._checker = self._checkers[0]
        self._language_label.set_text('<b>%s</b>' % self._lang_labels[0])
        self._language_label.set_use_markup(True)


gobject.type_register(SpellCheckWindow)
