[application_window]
maximized = boolean(default=False)
position = int_list(2, 2, default=list(0, 0))
show_main_toolbar = boolean(default=True)
show_statusbar = boolean(default=True)
show_video_toolbar = boolean(default=False)
size = int_list(2, 2, default=list(600, 371))
toolbar_style = toolbar_styles(default="DEFAULT")

[capitalization]
country = string(default="")
language = string(default="")
script = string(default="Latn")

[common_error]
check_human = boolean(default=True)
check_ocr = boolean(default=True)
country = string(default="")
language = string(default="")
script = string(default="Latn")

[debug]
editor = string(default="gedit")

[duration_adjust]
gap = float(min=0.0, default=0.0)
lengthen = boolean(default=True)
maximum = float(min=0.0, default=6.0)
minimum = float(min=0.0, default=1.5)
optimal = float(min=0.0, default=0.070)
shorten = boolean(default=False)
target = targets(default="CURRENT")
use_gap = boolean(default=True)
use_maximum = boolean(default=False)
use_minimum = boolean(default=True)

[editor]
custom_font = string(default="")
field_order = fields_list(default=list("NUMBER", "START", "END", "DURATION", "MAIN_TEXT", "TRAN_TEXT"))
framerate = framerates(default="FPS_24")
length_unit = length_units(default="EM")
limit_undo = boolean(default=False)
mode = modes(default="TIME")
show_lengths_cell = boolean(default=True)
show_lengths_edit = boolean(default=True)
undo_levels = integer(min=0, default=50)
use_custom_font = boolean(default=False)
visible_fields = fields_list(default=list("NUMBER", "START", "END", "DURATION", "MAIN_TEXT"))

[encoding]
fallbacks = string_list(default=list("utf_8", "cp1252"))
try_auto = boolean(default=True)
try_locale = boolean(default=True)
visibles = string_list(default=list("utf_8", "cp1252"))

[file]
align_method = align_methods(default="POSITION")
directory = string(default="")
encoding = string(default="")
format = formats(default="SUBRIP")
max_recent = integer(min=0, default=10)
newline = newlines(default="UNIX")

[framerate_convert]
target = targets(default="CURRENT")

[general]
version = string(default="")

[hearing_impaired]
country = string(default="")
language = string(default="")
script = string(default="Latn")

[line_break]
country = string(default="")
language = string(default="")
length_unit = length_units(default="EM")
max_deviation = float(default=0.16)
max_length = integer(min=1, default=28)
max_lines = integer(min=1, default=2)
max_skip_length = integer(min=1, default=28)
max_skip_lines = integer(min=1, default=3)
script = string(default="Latn")
skip_length = boolean(default=True)
skip_lines = boolean(default=True)

[output_window]
maximized = boolean(default=False)
position = int_list(2, 2, default=list(0, 0))
show = boolean(default=False)
size = int_list(2, 2, default=list(600, 371))

[position_shift]
target = targets(default="CURRENT")

[position_transform]
target = targets(default="CURRENT")

[preview]
custom_command = string(default="")
force_utf_8 = boolean(default=True)
offset = float(default=5.0)
use_custom = boolean(default=False)
video_player = players(default="MPLAYER")

[search]
fields = fields_list(default=list("MAIN_TEXT"))
ignore_case = boolean(default=True)
max_history = integer(min=0, default=10)
regex = boolean(default=False)
target = targets(default="CURRENT")

[spell_check]
field = fields(default="MAIN_TEXT")
language = string(default="en")
target = targets(default="CURRENT")

[subtitle_insert]
above = boolean(default=False)

[text_assistant]
field = fields(default="MAIN_TEXT")
pages = string_list(default=list())
remove_blank = boolean(default=True)
target = targets(default="CURRENT")
