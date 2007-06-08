[application_window]
maximized = boolean(default=False)
position = int_list(2, 2, default=list(0, 0))
show_main_toolbar = boolean(default=True)
show_statusbar = boolean(default=True)
show_video_toolbar = boolean(default=True)
size = int_list(2, 2, default=list(600, 371))
toolbar_style = TOOLBAR_STYLE(default="DEFAULT")

[debug]
editor = string(default="gedit")

[duration_adjust]
gap = float(min=0.0, default=0.0)
lengthen = boolean(default=True)
maximum = float(min=0.0, default=6.0)
minimum = float(min=0.0, default=1.5)
optimal = float(min=0.0, default=0.065)
shorten = boolean(default=False)
target = TARGET(default="CURRENT")
use_gap = boolean(default=True)
use_max = boolean(default=False)
use_min = boolean(default=True)

[editor]
font = string(default=None)
framerate = FRAMERATE(default="P24")
length_unit = LENGTH_UNIT(default="EM")
limit_undo = boolean(default=False)
mode = MODE(default="TIME")
show_lengths_cell = boolean(default=True)
show_lengths_edit = boolean(default=True)
undo_levels = integer(min=0, default=50)
use_default_font = boolean(default=True)
visible_cols = COLUMN_list(default=list("NUMBER", "START", "END", "DURATION", "MAIN_TEXT"))

[encoding]
fallbacks = string_list(default=list("utf_8", "cp1252"))
try_auto = boolean(default=True)
try_locale = boolean(default=True)
visibles = string_list(default=list("utf_8", "cp1252"))

[file]
directory = string(default=None)
encoding = string(default=None)
format = FORMAT(default="SUBRIP")
max_recent = integer(min=0, default=10)
newline = NEWLINE(default="UNIX")
smart_tran = boolean(default=True)
warn_ssa = boolean(default=True)

[framerate_convert]
target = TARGET(default="CURRENT")

[general]
version = string(default=None)

[open_dialog]
size = int_list(2, 2, default=list(0, 0))

[output_window]
maximized = boolean(default=False)
position = int_list(2, 2, default=list(0, 0))
show = boolean(default=False)
size = int_list(2, 2, default=list(600, 371))

[position_adjust]
target = TARGET(default="CURRENT")

[position_shift]
target = TARGET(default="CURRENT")

[preview]
custom_command = string(default=None)
offset = float(default=5.0)
use_predefined = boolean(default=True)
video_player = VIDEO_PLAYER(default="MPLAYER")

[search]
cols = COLUMN_list(default=list("MAIN_TEXT"))
ignore_case = boolean(default=True)
max_history = integer(min=0, default=10)
patterns = string_list(default=list())
regex = boolean(default=False)
replacements = string_list(default=list())
target = TARGET(default="CURRENT")

[spell_check]
col = COLUMN(default="MAIN_TEXT")
lang = string(default="en")
target = TARGET(default="CURRENT")

[subtitle_insert]
above = boolean(default=False)
amount = integer(min=1, default=1)
