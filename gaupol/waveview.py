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

"""User interface container and controller for :class:`aeidon.Project`."""

import aeidon
import gaupol
import os
import sys
import cairo
import traceback
import argparse

from aeidon.i18n   import _
from gi.repository import Gtk, GObject, Gst, Gdk

# gi.require_version('Gst', '1.0')
# from gi.repository import Gst, GObject

__all__ = ("Waveview",)

TMP_PATH = "/tmp/"
TMP_EXT = ".gaupol"

"""
for 16 bits in 16 bits, signed, little endian:

gst-launch-1.0 filesrc location=filename ! \ 
 decodebin ! audioconvert ! audioresample ! \
 audio/x-raw, channels=1, rate=16000, format=S16LE ! \
 filesink location=out.raw

for 8 bits, 8K/sec:

gst-launch-1.0 filesrc location=filename ! \
    decodebin ! audioconvert ! \
    audioresample ! \
    audio/x-raw, channels=1, rate=8000, format=S8 ! \
    filesink location=fileout.raw
"""

AUDIO_SAMPLES_PER_SECOND = 8000
DECIMATE_FACTOR = 80
DISP_SAMPLES_PER_SECOND = AUDIO_SAMPLES_PER_SECOND / DECIMATE_FACTOR
DISP_SPAM_IN_SECONDS = 10
DISP_SPAM_IN_SAMPLES = DISP_SPAM_IN_SECONDS * DISP_SAMPLES_PER_SECOND

WAVE_H_MARGINS = 0.05     # 5% each left/right side
WAVE_V_MARGINS = 0.10     # 10% each top/bottom

THEMES = { \
    'dark': { \
        'wave': {'r': 255, 'g': 255, 'b': 0}, \
        'pos_cursor' : {'r': 255, 'g': 0, 'b': 0} \
    } \
}


class GraphicArea(Gtk.DrawingArea):
    """ This class is a Drawing Area"""
    def __init__(self, parent):
        super(GraphicArea,self).__init__()
        self.parent = parent
        self.spam_in_samples = DISP_SPAM_IN_SAMPLES
        self.set_theme('dark')

        self.connect("draw", self.on_draw)
        GObject.timeout_add(50, self.tick) # Go call tick every 50 whatsits.

        self.disp_samples = None
        self.sample_pos = -1
        self.last_sample_pos = 0
        self.sample_base = 0 # sample index at the start of the left side

        ## Register events callbacks
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect('button-press-event', self.event_cb)

        # self.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        # self.connect('motion-notify-event', self.on_motion)


    #######################################
    #
    #               draw_wave
    #
    #######################################
    def draw_wave(self, width, height):
        #self.ctx.set_source_rgb(0, 0, 0)
        self.set_color(self.color_wave)
        left_offset = width * WAVE_H_MARGINS
        right_max = width - left_offset
        x_g_span = right_max - left_offset
        y_span = height - (height * WAVE_V_MARGINS * 2)

        if self.disp_samples == None:
            return


        if self.sample_pos > self.last_sample_pos:
            increasing = True
            self.last_sample_pos = self.sample_base
        
        # point to the next frame if pos beyond max
        if self.sample_pos - self.sample_base > self.spam_in_samples or self.sample_base > self.sample_pos:
            v = self.sample_pos / self.spam_in_samples
            if v == 0:
                v = 1
            v = int(v) * self.spam_in_samples
            self.sample_base = int(v)

        max_x = self.spam_in_samples
        if max_x >= len(self.disp_samples):
            max_x = len(self.disp_samples) - 1
        offset_x = x_g_span/max_x
        x = left_offset
        i = 0

        #self.ctx.set_line_width(0.02)
        self.set_color(self.color_wave)
        self.ctx.move_to(x, 0)
        while x <= right_max:
            if i + self.sample_base >= len(self.disp_samples):
                break
            line_len = self.disp_samples[i + self.sample_base] * y_span
            if line_len < 3:
                line_len = 3
            y_start = (height - line_len) / 2
            y_end = y_start + line_len
            self.ctx.move_to(x, y_start)
            self.ctx.line_to(x, y_end)
            self.ctx.stroke()
            i += 1
            x += offset_x

        # draw cursor
        if self.sample_pos >= 0 and self.sample_pos - self.sample_base < max_x:
            self.set_color(self.color_pos_cursor)
            x = (self.sample_pos - self.sample_base) * offset_x + left_offset
            self.ctx.move_to(x, height)
            self.ctx.line_to(x, 0)
            self.ctx.stroke()
    #######################################
    #
    #               events
    #
    #######################################
    @aeidon.deco.export
    def on_left_click(self, x,y):
        print("left-click event " + str(x) + ", " + str(y))
        self.parent.emit("request-set-seekbar", 0.5)

    def on_right_click(self, x,y):
        print("right-click event " + str(x) + ", " + str(y))

    def on_motion(self, widget, ev):
        print("on motion event " + str(ev.x) + ", " + str(ev.y))

    def event_cb(self, widget, ev):
        #if ev.type == Gdk.EventMask.BUTTON_PRESS_MASK:
        if ev.button == 1:
            self.on_left_click(ev.x, ev.y)
        elif ev.button == 3:
            self.on_right_click(ev.x, ev.y)
        # elif ev.type == Gdk.EventMask.MOTION_NOTIFY_MASK: #POINTER_MOTION_MASK:
        #     self.on_motion(ev.x, ev.y)


    def set_theme(self, t):
        self.color_wave = THEMES[t]['wave']
        self.color_pos_cursor = THEMES[t]['pos_cursor']

    def set_data(self, data):
        self.disp_samples = data

    def set_position(self, pos):
        if self.disp_samples == None:
            return
        # pos is fraction of the total duration
        self.sample_pos = int(len(self.disp_samples) * pos)

    def tick(self):
        ## This invalidates the graphic area, causing the "draw" event to fire.
        rect = self.get_allocation()
        #self.get_window().invalidate_rect(rect, True)
        #w = self.get_window()
        #w.invalidate_rect(rect, True)
        #self.gtk_widget_queue_draw_area()
        self.queue_draw()
        return True # Causes timeout to tick again.

    def set_color(self, c):
        self.ctx.set_source_rgb(c['r'], c['g'], c['b'])

    ## When the "draw" event fires, this is run
    def on_draw(self, widget, event):
        self.ctx = self.get_window().cairo_create()
        geom = self.get_window().get_geometry()
        self.draw_wave(geom.width, geom.height)
    


#ref: https://github.com/jackersson/gst-python-tutorials/blob/master/launch_pipeline/pipeline_with_parse_launch.py

class CreateCache():
    def __init__(self, file_in, file_out):
        super(CreateCache,self).__init__()
        # check if there is a cache already
        if os.path.exists(file_out):
            # check if newer than video file
            ts_out = os.stat(file_out).st_mtime
            ts_in = os.stat(file_in).st_mtime
            if ts_out > ts_in:
                # we have a valid cache file
                print("wave cache found")
                return

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
            print("End of stream")
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
            print("Progress message " + str(p) + "%")
            self.progress.set_fraction(p/100)

        else:
            print(mtype)

        return True


class Progress(Gtk.Window):
    def __init__(self):
        super(Progress, self).__init__()
        self.set_default_size(400,200)
        self.set_title("Gaupol Progress")
        vbox = Gtk.VBox()
        label = Gtk.Label("Creating cache for wave graphic")
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
    def __init__(self, parent):
        super(Waveview,self).__init__()
        self.parent = parent
        self.graphic_area = GraphicArea(parent)
        #self.graphic_area.set_size_request(0, 100)
        self.top_container = Gtk.HBox(spacing=6)
        self.top_container.set_homogeneous(True)

        self.vbox = Gtk.VBox(spacing=6)
        # b = Gtk.Button("Dummy 1")
        # self.vbox.pack_start(b, True, False, 0)
        # b = Gtk.Button("Dummy 2")
        # self.vbox.pack_start(b, True, True, 0)

        self.top_container.pack_start(self.graphic_area, True, True, 0)
        #self.top_container.pack_start(self.vbox, True, True, 0)
        self.top_container.show_all()


    def getWidget(self):
        return self.top_container

    def set_position(self, pos):
        self.graphic_area.set_position(pos)

    def create_data(self, path):
        tmp_name = TMP_PATH + os.path.basename(path) + TMP_EXT
        CreateCache(path, tmp_name)

        f = open(tmp_name, 'rb')
        d = bytearray(f.read())  # maybe save d as self.audio_samples for scrubbing
        f.close()

        # maybe run an IIR low pass before decimation?

        # decimate date
        i = 0
        _len = len(d)
        samples = []
        max = 0

        while (i < _len):
            b = d[i]
            if b > 127:
                b = 256 - b
            samples.append(b)
            if b > max:
                max = b
            i += DECIMATE_FACTOR
        #print("n samples = " + str(len(samples)))
        #print ("DISP_SAMPLES_PER_SECOND = " + str(DISP_SAMPLES_PER_SECOND))

        ## normalize
        _len = len(samples)
        i = 0
        f = 1.0 / max
        #print("max = " + str(max) + ", f = " + str(f))
        while (i < _len):
            samples[i] *= f
            i += 1
        self.disp_samples = samples
        self.graphic_area.set_data(samples)
        #print(samples)




