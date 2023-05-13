# -*- coding: utf-8 -*-

# Copyright (C) 2023 Varanda Labs Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Wave viewer - an audio visualizer."""

import aeidon
import gaupol
import os
import sys
import cairo
import traceback
import argparse

from aeidon.i18n   import _
from gi.repository import Gtk, GObject, Gst, Gdk

__all__ = ("Waveview",)

TMP_PATH = "/tmp/"
TMP_AUDIO_PCM = ".audio.gaupol"
TMP_DISPLAY_PCM8_SAMPLES = ".display.gaupol"

AUDIO_SAMPLES_PER_SECOND = 8000
DECIMATE_FACTOR = 80
DISP_SAMPLES_PER_SECOND = AUDIO_SAMPLES_PER_SECOND / DECIMATE_FACTOR
DISP_SPAN_IN_SECONDS = 10
DISP_SPAN_IN_SAMPLES = DISP_SPAN_IN_SECONDS * DISP_SAMPLES_PER_SECOND

WAVE_H_MARGINS = 0.05     # 5% each left/right side
WAVE_V_MARGINS = 0.10     # 10% each top/bottom

BAR_HEIGTH = 20
BAR_Y_OFFSET = 10
BAR_TEXT_X_OFFSET = 4
BAR_TEXT_Y_OFFSET = 4

SPAN_LABEL_X_OFFSET = 14
SPAN_LABEL_Y_OFFSET = 14

DRAG_BAR_ST__IDLE = 0
DRAG_BAR_ST__START_BT_DOWN = 1
DRAG_BAR_ST__DRAGGING = 2


THEMES = { \
    'Dark': { \
        'wave': {'r': 1, 'g': 1, 'b': 0}, \
        'pos_cursor' : {'r': 1, 'g': 0, 'b': 0}, \
        'bar' : {'r': 37/256, 'g': 137/256, 'b': 157/256}, \
        'bar_selected' : {'r': 181/256, 'g': 233/256, 'b': 243/256}, \
        'dash_line_selected' : {'r': 181/256, 'g': 233/256, 'b': 243/256}, \
        'bar_text' : {'r': 255/256, 'g': 255/256, 'b': 255/256}, \
        'bar_text_selected' : {'r': 98/256, 'g': 92/256, 'b': 13/256}, \
        'labels' : {'r': 0xff/256, 'g': 0xea/256, 'b': 0x7b/256}, \
    }, \
    'Light': { \
        'wave': {'r': 2/256, 'g': 7/256, 'b': 0x71/256}, \
        'pos_cursor' : {'r': 1, 'g': 0, 'b': 0}, \
        'bar' : {'r': 37/256, 'g': 137/256, 'b': 157/256}, \
        'bar_selected' : {'r': 181/256, 'g': 233/256, 'b': 243/256}, \
        'dash_line_selected' : {'r': 4/256, 'g': 0xbe/256, 'b': 0x32/256}, \
        'bar_text' : {'r': 255/256, 'g': 255/256, 'b': 255/256}, \
        'bar_text_selected' : {'r': 98/256, 'g': 92/256, 'b': 13/256}, \
        'labels' : {'r': 0x2/256, 'g': 0x3/256, 'b': 0x71/256}, \
    } \
}

_waveview_instance = None

def get_waveview_instance():
    return _waveview_instance


class SignalPoster(aeidon.Observable): 
    signals = (
        "wave-req-seek",
        "wave-subtitle-change",
        "wave-req-set-focus",
        "wave-time-edit-end",
    )
    def __init__(self):
        """Initialize an :class:`SignalPoster` instance."""
        aeidon.Observable.__init__(self)

    def emit_seek_request(self, pos):
        self.emit("wave-req-seek", pos)

    def emit_subtitle_change(self, pos):
        self.emit("wave-subtitle-change", pos)

    def emit_focus_set(self, row):
        self.emit("wave-req-set-focus", row)
    
    def emit_time_edit_end(self, is_end, row, val_seconds):
        self.emit("wave-time-edit-end", is_end, row, val_seconds)

class GraphicArea(Gtk.DrawingArea):
    """ This class is a Drawing Area"""
    def __init__(self, poster, is_visible):
        super(GraphicArea,self).__init__()
        self.is_visible = is_visible
        self.calc = aeidon.Calculator()
        self.poster = poster
        self.subtitles = None
        self.span_in_samples = DISP_SPAN_IN_SAMPLES
        self.span_in_time = self.span_in_samples / DISP_SAMPLES_PER_SECOND
        self.set_theme('Dark')

        self.connect("draw", self.on_draw)
        if is_visible == True:
            GObject.timeout_add(50, self.on_timer) # Go call on_timer every 50 whatsits.

        self.disp_samples = None
        self.sample_pos = -1
        self.last_sample_pos = 0
        self.sample_base = 0 # sample index at the start of the left side
        self.duration = 0
        self.width = 0
        self.x_g_span = 0
        self.bars_cache = None
        self.selected_rows = [0]

        ## Register events callbacks
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect('button-press-event', self.on_bt_press)

        self.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.connect('button-release-event', self.on_bt_release)

        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.connect('motion-notify-event', self.on_motion)

        self.create_bars_cache()
        self.drag_bar_state = DRAG_BAR_ST__IDLE
        self.drag_bar_init_x = 0
        self.drag_bar_timer = 0
        self.drag_end_side = False
        self.drag_bar_row = -1

    def set_visible(self, v):
        # When wave viewer become visible turn on the draw timer
        if self.is_visible != v:
            self.is_visible = v
            if v == True:
                GObject.timeout_add(50, self.on_timer) # Go call on_timer every 50 milliseconds.

    def init_view_signals (self, view):
        view.connect_selection_changed(self.on_focus_changed)

    def set_span(self, secs):
        self.span_in_time = secs
        self.span_in_samples = self.span_in_time * DISP_SAMPLES_PER_SECOND

    def on_focus_changed(self, view):
        self.selected_rows = []
        row_paths = view.get_selected_rows()[1]
        for r in row_paths:
            for rr in r:
                self.selected_rows.append(rr)

    def get_pixel_to_time(self, x):
        f = self.span_in_time / self.x_g_span
        return x * f

    def get_click_time(self, x):
        xx = (x - self.width * WAVE_H_MARGINS) / self.x_g_span
        d = xx * self.span_in_time
        d += (self.sample_base/100)
        if d < 0:
            return 0
        return d

    def get_x_from_time(self, d):
        d -= (self.sample_base/100)
        d /= self.span_in_time
        d *= self.x_g_span
        d += self.width * WAVE_H_MARGINS
        return d
    
    #######################################
    #
    #               draw_wave
    #
    #######################################
    def draw_wave(self, width, height):
        ctx = self.ctx # speed up access to ctx
        ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(12)
        self.set_color(self.color_wave)
        t = "span: " + str(self.span_in_time) + " secs"
        ctx.move_to(SPAN_LABEL_X_OFFSET, height - SPAN_LABEL_Y_OFFSET)
        ctx.show_text(t)
        
        self.set_color(self.color_wave)
        left_offset = width * WAVE_H_MARGINS
        right_max = width - left_offset
        self.x_g_span = right_max - left_offset
        y_span = height - (height * WAVE_V_MARGINS * 2)

        if self.disp_samples == None:
            return


        if self.sample_pos > self.last_sample_pos:
            increasing = True
            self.last_sample_pos = self.sample_base
        
        # point to the next frame if pos beyond max
        if self.sample_pos - self.sample_base > self.span_in_samples or self.sample_base > self.sample_pos:
            v = self.sample_pos / self.span_in_samples
            if v == 0:
                v = 1
            v = int(v) * self.span_in_samples
            if self.sample_base != int(v):
                self.create_bars_cache()
                self.sample_base = int(v)

        max_x = self.span_in_samples
        if max_x >= len(self.disp_samples):
            max_x = len(self.disp_samples) - 1
        offset_x = self.x_g_span/max_x
        x = left_offset
        i = 0

        #ctx.set_line_width(0.02)
        self.set_color(self.color_wave)
        ctx.move_to(x, 0)
        while x <= right_max:
            if i + self.sample_base >= len(self.disp_samples):
                break
            line_len = self.disp_samples[i + self.sample_base] * y_span
            if line_len < 3:
                line_len = 3
            y_start = (height - line_len) / 2
            y_end = y_start + line_len
            ctx.move_to(x, y_start)
            ctx.line_to(x, y_end)
            ctx.stroke()
            i += 1
            x += offset_x

        ############### draw cursor #############
        if self.sample_pos >= 0 and self.sample_pos - self.sample_base < max_x:
            self.set_color(self.color_pos_cursor)
            x = (self.sample_pos - self.sample_base) * offset_x + left_offset
            ctx.move_to(x, height)
            ctx.line_to(x, 0)
            ctx.stroke()

        ########### draw subtitle bars ##########
        #
        # there is a chance that the following code will be slow.
        # we may need to cache the visible bars and update the cache upon 
        # notification for changes.
        #

        if self.bars_cache != None:
            sel = False
            for b in self.bars_cache:
                sel = False
                if b['row'] in self.selected_rows:
                    self.set_color(self.color_bar_selected)
                    sel = True
                else:
                    self.set_color(self.color_bar)
                ctx.rectangle(b['x0'], BAR_Y_OFFSET, b['bar_len'], BAR_HEIGTH)
                ctx.fill()
                if sel == True:
                    self.set_color(self.color_dash_line_selected)
                    ctx.set_dash ([6,3])
                    ctx.set_line_width(1)
                    ctx.move_to(b['x0'] + 1, BAR_Y_OFFSET + BAR_HEIGTH)
                    ctx.line_to(b['x0'] + 1, height)
                    ctx.stroke()
                    ctx.move_to(b['x1'] - 1, BAR_Y_OFFSET + BAR_HEIGTH)
                    ctx.line_to(b['x1'] - 1, height)
                    ctx.stroke()
                if len(b['text']) > 0:
                    ctx.move_to(b['x0'] + BAR_TEXT_X_OFFSET, BAR_HEIGTH + BAR_TEXT_Y_OFFSET)
                    if sel == True:
                        self.set_color(self.color_bar_text_selected)
                    else:
                        self.set_color(self.color_bar_text)
                    ctx.show_text(b['text'])

    def create_bars_cache(self):
        self.bars_cache = []

        if self.subtitles != None:
            visible_start = self.sample_base/100
            visible_end = visible_start + self.span_in_time
            id = 0
            for s in self.subtitles:
                if s.start_seconds > visible_end:
                    break
                start = s.start_seconds
                if s.start_seconds >= visible_start or s.end_seconds < visible_end:
                    if s.start_seconds < visible_start:
                        x0 = 0
                    else:
                        x0 = self.get_x_from_time(s.start_seconds)
                    x1 = self.get_x_from_time(s.end_seconds)
                    bar_len = x1 - x0
                    t = ""
                    if bar_len > 40:
                        t = s.main_text[:5]
                    e = {   'row':id, 
                            'x0':x0, 
                            'x1':x1, 
                            'bar_len': bar_len, 
                            'text': t, 
                            'start_seconds': s.start_seconds, 
                            'end_seconds' : s.end_seconds }
                    self.bars_cache.append(e)
                id += 1

    # ret: int row, bool is_end_side
    def get_pointed_bar_id(self, x, y):
        if self.bars_cache == None:
            return -1, False
        if len(self.bars_cache) == 0:
            return -1, False
        if y < BAR_Y_OFFSET:
            return -1, False
        if y > BAR_Y_OFFSET + BAR_HEIGTH:
            return -1, False
        for b in self.bars_cache:
            if x >= b['x0'] and x <= b['x1']:
                is_end_side = False
                if x > b['x0'] + ((b['x1'] - b['x0']) / 2):
                    is_end_side = True
                return b['row'], is_end_side
        return -1, False

    #######################################
    #
    #               events
    #
    #######################################
    @aeidon.deco.export
    def on_left_click(self, x,y):
        t = self.get_click_time(x)
        bar_id, self.drag_end_side = self.get_pointed_bar_id(x,y)
        
        if bar_id >=0:
            self.poster.emit_focus_set(bar_id)
            self.drag_bar_state = DRAG_BAR_ST__DRAGGING
            self.drag_bar_row = bar_id
            self.drag_bar_init_x = x
            if self.drag_end_side == True:
                self.drag_bar_base_value = self.subtitles[bar_id].end_seconds
            else:
                self.drag_bar_base_value = self.subtitles[bar_id].start_seconds
        else:
            self.poster.emit_seek_request( t)

    def on_right_click(self, x,y):
        # placeholder
        # print("right-click event " + str(x) + ", " + str(y))
        # print("TODO: implement context menu")
        pass


    def on_motion(self, widget, ev):
        if self.drag_bar_state == DRAG_BAR_ST__DRAGGING:
            delta = ev.x - self.drag_bar_init_x
            delta_time = - self.get_pixel_to_time(delta)
            v = self.drag_bar_base_value - delta_time
            if self.drag_end_side == True:
                if v > self.subtitles[self.drag_bar_row].start_seconds + 0.3:
                    self.subtitles[self.drag_bar_row].end_seconds = v
            else:
                if v < self.subtitles[self.drag_bar_row].end_seconds - 0.3:
                    self.subtitles[self.drag_bar_row].start_seconds = v
            self.poster.emit_subtitle_change(self.drag_bar_row)

    def on_bt_press(self, widget, ev):
        if ev.button == 1:
            self.on_left_click(ev.x, ev.y)

        elif ev.button == 3:
            self.on_right_click(ev.x, ev.y)

    def on_bt_release(self, widget, ev):
        if ev.button == 1:
            if self.drag_bar_state == DRAG_BAR_ST__IDLE:
                return
            self.drag_bar_state = DRAG_BAR_ST__IDLE
            if self.drag_bar_row >=0:
                if self.drag_end_side:
                    t =self.subtitles[self.drag_bar_row].end_seconds
                    self.subtitles[self.drag_bar_row].end_seconds = self.drag_bar_base_value # revert time to its initial value
                    self.poster.emit_time_edit_end(self.drag_end_side, self.drag_bar_row, t)
                else:
                    t = self.subtitles[self.drag_bar_row].start_seconds
                    self.subtitles[self.drag_bar_row].start_seconds = self.drag_bar_base_value # revert time to its initial value
                    self.poster.emit_time_edit_end(self.drag_end_side, self.drag_bar_row, t)
                self.drag_bar_row = -1

    def set_theme(self, t):
        self.color_wave = THEMES[t]['wave']
        self.color_pos_cursor = THEMES[t]['pos_cursor']
        self.color_bar = THEMES[t]['bar']
        self.color_bar_selected = THEMES[t]['bar_selected']
        self.color_bar_text = THEMES[t]['bar_text']
        self.color_bar_text_selected = THEMES[t]['bar_text_selected']
        self.color_labels = THEMES[t]['labels']
        self.color_dash_line_selected = THEMES[t]['dash_line_selected']

    def set_data(self, data):
        self.disp_samples = data

    def set_position(self, position, duration, subtitles):
        self.subtitles = subtitles
        self.create_bars_cache()
        if self.disp_samples == None or duration <= 0:
            return
        
        self.duration = duration
        self.sample_pos = int(len(self.disp_samples) * (position/duration))

    def on_timer(self):
        ## This invalidates the graphic area, causing the "draw" event to fire.
        if self.is_visible == True:
            self.queue_draw()
        return self.is_visible # Causes timeout to on_timer again when visible.

    def set_color(self, c):
        self.ctx.set_source_rgb(c['r'], c['g'], c['b'])

    ## When the "draw" event fires, this is ran
    def on_draw(self, widget, event):
        self.ctx = self.get_window().cairo_create()
        geom = self.get_window().get_geometry()
        self.width = geom.width
        self.draw_wave(geom.width, geom.height)
    

#ref: https://github.com/jackersson/gst-python-tutorials/blob/master/launch_pipeline/pipeline_with_parse_launch.py

class CreateCache():
    def __init__(self, file_in, file_out):
        p = Progress()
        self.progress = p.get_progress()

        DEFAULT_PIPELINE = "filesrc location=FILEIN ! decodebin ! progressreport update-freq=1 silent=true ! audioconvert ! audioresample ! audio/x-raw, channels=1, rate=RATE, format=S8 ! filesink location=FILEOUT"
        default_pipeline = DEFAULT_PIPELINE.replace("FILEIN", file_in)
        default_pipeline = default_pipeline.replace("FILEOUT", file_out)
        default_pipeline = default_pipeline.replace("RATE", str(AUDIO_SAMPLES_PER_SECOND))

        pipeline = Gst.parse_launch(default_pipeline)
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        pipeline.set_state(Gst.State.PLAYING)

        # Init GObject loop to handle Gstreamer Bus Events
        loop = GObject.MainLoop()

        bus.connect("message", self.on_message, loop)

        try:
            loop.run()
        except Exception:
            traceback.print_exc()
            p.hide()
            p = None
            loop.quit()

        # Stop Pipeline
        pipeline.set_state(Gst.State.NULL)
        p.hide()
        p = None


    def on_message(self, bus: Gst.Bus, message: Gst.Message, loop: GObject.MainLoop):
        mtype = message.type
        """
            Gstreamer Message Types and how to parse
            https://lazka.github.io/pgi-docs/Gst-1.0/flags.html#Gst.MessageType
        """
        if mtype == Gst.MessageType.EOS:
            loop.quit()

        elif mtype == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(err, debug)
            loop.quit()

        elif mtype == Gst.MessageType.WARNING:
            err, debug = message.parse_warning()
            print(err, debug)

        elif mtype == Gst.MessageType.ELEMENT:
            b,p = message.get_structure().get_int("percent")
            self.progress.set_fraction(p/100)

        return True


class Progress(Gtk.Window):
    def __init__(self):
        super(Progress, self).__init__()
        self.set_default_size(400,200)
        self.set_title("Gaupol Progress")
        vbox = Gtk.VBox()
        label = Gtk.Label("Creating cache for audio visualizer")
        vbox.pack_start(label, expand = True, fill = True, padding = 6)
        self.progress = Gtk.ProgressBar()
        self.progress.set_margin_bottom(100)
        self.progress.set_margin_right(10)
        self.progress.set_margin_left(10)
        vbox.pack_start(self.progress, expand = True, fill = True, padding = 4)
        self.add(vbox)
        self.show_all()

    def get_progress(self):
        return self.progress
    
class Waveview():
    """ This class is a Drawing Area"""
    def __init__(self, is_visible):
        global _waveview_instance
        self.is_visible = is_visible
        self.poster = SignalPoster()
        self.graphic_area = GraphicArea(self.poster, is_visible)
        self.top_container = Gtk.HBox(spacing=6)
        self.top_container.set_homogeneous(True)
        self.vbox = Gtk.VBox(spacing=6)
        self.top_container.pack_start(self.graphic_area, True, True, 0)
        self.top_container.show_all()
        _waveview_instance = self
        self.disp_samples = None
        self.video_file_path = None

    def set_visible(self, v):
        self.is_visible = v
        if v == True:
            if self.video_file_path != None:
                self.create_data(self.video_file_path)
        self.graphic_area.set_visible(v)

    def set_theme(self, t):
        self.graphic_area.set_theme(t)

    def set_span(self, span):
        secs = 10
        if span == "20 Seconds":
            secs = 20
        self.graphic_area.set_span(secs)

    def init_view_signals (self, view):
        self.graphic_area.init_view_signals(view)

    def getWidget(self):
        return self.top_container

    def set_position(self, position, duration, subtitles):
        self.graphic_area.set_position(position, duration, subtitles)
        self.subtitles = subtitles

    def decimate_and_normalize(self, decimation, bytes):
        # decimate date, output: bytes, samples
        # returns: bytes_output, samples
        # if decimation ==  1 bytes_output == empty 
        i = 0
        _len = len(bytes)
        samples = []
        max = 0
        bytes_output = bytearray()

        while (i < _len):
            b = bytes[i]
            if b > 127:
                b = 256 - b
            samples.append(b)
            if b > max:
                max = b
            if decimation > 1:
                bytes_output.append(bytes[i])
            i += decimation

        ## normalize
        _len = len(samples)
        i = 0
        f = 1.0 / max
        while (i < _len):
            samples[i] *= f
            i += 1
        return bytes_output, samples

    def create_data(self, path):
        if self.disp_samples != None:
            #ignore if we already have samples
            return

        if self.is_visible == False:
            #postpone for when it becomes visible for the first time
            self.video_file_path = path
            return
        
        tmp_display_samples_file = TMP_PATH + os.path.basename(path) + TMP_DISPLAY_PCM8_SAMPLES

        ## check if a valid cache is available
        if os.path.exists(tmp_display_samples_file):
            # check if newer than video file
            ts_out = os.stat(tmp_display_samples_file).st_mtime
            ts_in = os.stat(path).st_mtime
            if ts_out > ts_in:
                # we have a valid cache file
                f = open(tmp_display_samples_file, 'rb')
                d = bytearray(f.read())  # maybe save d as self.audio_samples for scrubbing
                f.close()

                bytes_out, samples = self.decimate_and_normalize(1, d)
                self.disp_samples = samples
                self.graphic_area.set_data(samples)
                return
            

        tmp_audio_file = TMP_PATH + os.path.basename(path) + TMP_AUDIO_PCM
        CreateCache(path, tmp_audio_file)

        f = open(tmp_audio_file, 'rb')
        d = bytearray(f.read())  # maybe save d as self.audio_samples for scrubbing
        f.close()

        bytes_out, samples = self.decimate_and_normalize(DECIMATE_FACTOR, d)

        ## save cache
        f = open(tmp_display_samples_file, "wb")
        for byte in bytes_out:
            f.write(byte.to_bytes(1, byteorder='big'))
        f.close()

        ## Delete audio file (unless we implement scrubbing later on)
        try:
            os.remove(tmp_audio_file)
        except:
            pass

        self.disp_samples = samples
        self.graphic_area.set_data(samples)





