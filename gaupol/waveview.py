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
from gi.repository import Gtk, GObject, Gst

# gi.require_version('Gst', '1.0')
# from gi.repository import Gst, GObject

__all__ = ("Waveview",)

TMP_PATH = "/tmp/"
TMP_EXT = ".gaupol.$$$"

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

#ref: https://github.com/jackersson/gst-python-tutorials/blob/master/launch_pipeline/pipeline_with_parse_launch.py

class CreateCache():
    def __init__(self, file_in, file_out, progress):
        super(CreateCache,self).__init__()
        self.progress = progress

        DEFAULT_PIPELINE = "filesrc location=FILEIN ! decodebin ! progressreport update-freq=1 silent=true ! audioconvert ! audioresample ! audio/x-raw, channels=1, rate=8000, format=S8 ! filesink location=FILEOUT"
        default_pipeline = DEFAULT_PIPELINE.replace("FILEIN", file_in)
        default_pipeline = default_pipeline.replace("FILEOUT", file_out)

        ap = argparse.ArgumentParser()
        ap.add_argument("-p", "--pipeline", required=False,
                        default=default_pipeline, help="Gstreamer pipeline without gst-launch")

        args = vars(ap.parse_args())

        command = args["pipeline"]

        pipeline = Gst.parse_launch(command)
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
            loop.quit()

        # Stop Pipeline
        pipeline.set_state(Gst.State.NULL)


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

AUDIO_SAMPLES_PER_SECOND = 8000
DECIMATE_FACTOR = 80 * 4
SAMPLES_PER_SECOND = AUDIO_SAMPLES_PER_SECOND / DECIMATE_FACTOR
SPAM_IN_SECONDS = 10
SPAM_IN_SAMPLES = SPAM_IN_SECONDS * SAMPLES_PER_SECOND


class GraphicArea(Gtk.DrawingArea):
    """ This class is a Drawing Area"""
    def __init__(self):
        super(GraphicArea,self).__init__()
        ## Connect to the "draw" signal
        self.connect("draw", self.on_draw)
        ## This is what gives the animation life!
        GObject.timeout_add(50, self.tick) # Go call tick every 50 whatsits.


        ## x,y is where I'm at
        self.x, self.y = 25, -25
        ## rx,ry is point of rotation
        self.rx, self.ry = -10, -25
        ## rot is angle counter
        self.rot = 0
        ## sx,sy is to mess with scale
        self.sx, self.sy = 1, 1

    def tick(self):
        ## This invalidates the graphic area, causing the "draw" event to fire.
        rect = self.get_allocation()
        #self.get_window().invalidate_rect(rect, True)
        #w = self.get_window()
        #w.invalidate_rect(rect, True)
        #self.gtk_widget_queue_draw_area()
        self.queue_draw()
        return True # Causes timeout to tick again.

    ## When the "draw" event fires, this is run
    def on_draw(self, widget, event):
        self.cr = self.get_window().cairo_create()
        ## Call our draw function to do stuff.
        geom = self.get_window().get_geometry()
        self.draw(geom.width, geom.height)

    def draw(self, width, height):
        ## A shortcut
        cr = self.cr

        ## First, let's shift 0,0 to be in the center of page
        ## This means:
        ##  -y | -y
        ##  -x | +x
        ## ----0------
        ##  -x | +x
        ##  +y | +y

        matrix = cairo.Matrix(1, 0, 0, 1, width/2, height/2)
        cr.transform(matrix) # Make it so...

        ## Now save that situation so that we can mess with it.
        ## This preserves the last context(the one at 0,0)
        ## and let's us do new stuff.
        cr.save()

        ## Now attempt to rotate something around a point
        ## Use a matrix to change the shape's position and rotation.

        ## First, make a matrix. Don't look at me, I only use this stuff :)
        ThingMatrix = cairo.Matrix(1, 0, 0, 1, 0, 0)

        ## Next, move the drawing to it's x,y
        cairo.Matrix.translate(ThingMatrix, self.x, self.y)
        cr.transform(ThingMatrix) # Changes the context to reflect that

        ## Now, change the matrix again to:
        cairo.Matrix.translate(ThingMatrix, self.rx, self.ry) # move it all to point of rotation
        cairo.Matrix.rotate(ThingMatrix, self.rot) # Do the rotation
        cairo.Matrix.translate(ThingMatrix, -self.rx, -self.ry) # move it back again
        cairo.Matrix.scale(ThingMatrix, self.sx, self.sy) # Now scale it all
        cr.transform(ThingMatrix) # and commit it to the context

        ## Now, whatever is draw is "under the influence" of the
        ## context and all that matrix magix we just did.
        self.drawCairoStuff(cr)

        ## Let's inc the angle a little
        self.rot += 0.1

        ## Now mess with scale too
        self.sx += 0 # Change to 0 to see if rotation is working...
        if self.sx > 4: self.sx=0.5
        self.sy = self.sx

        ## We restore to a clean context, to undo all that hocus-pocus
        cr.restore()

        ## Let's draw a crosshair so we can identify 0,0
        ## Drawn last to be above the red square.
        self.drawcross(cr)

    def drawCairoStuff(self, cr):
        ## Thrillingly, we draw a red rectangle.
        ## It's drawn such that 0,0 is in it's center.
        cr.rectangle(-25, -25, 50, 50)
        cr.set_source_rgb(1, 0, 0)
        cr.fill()
        ## Now a visual indicator of the point of rotation
        ## I have no idea(yet) how to keep this as a
        ## tiny dot when the entire thing scales.
        cr.set_source_rgb(1, 1, 1)
        cr.move_to(self.rx, self.ry)
        cr.line_to(self.rx+1, self.ry+1)
        cr.stroke()

    def drawcross(self, ctx):
        ## Also drawn around 0,0 in the center
        ctx.set_source_rgb(0, 0, 0)
        ctx.move_to(0,10)
        ctx.line_to(0, -10)
        ctx.move_to(-10, 0)
        ctx.line_to(10, 0)
        ctx.stroke()

class Progress(Gtk.Window):
    def __init__(self):
        super(Progress, self).__init__()
        self.set_default_size(400,200)
        self.set_title("Gaupol Progress")
        vbox = Gtk.VBox()
        label = Gtk.Label("Loading/Parsing Video File")
        vbox.pack_start(label, expand = True, fill = True, padding = 10)
        self.progress = Gtk.ProgressBar()
        vbox.pack_start(self.progress, expand = True, fill = True, padding = 10)
        self.add(vbox)
        self.show_all()

    def get_progress(self):
        return self.progress

class Waveview():
    """ This class is a Drawing Area"""
    def __init__(self):
        super(Waveview,self).__init__()
        self.graphic_area = GraphicArea()
        self.top_container = Gtk.HBox(spacing=6)

        self.vbox = Gtk.VBox(spacing=6)
        b = Gtk.Button("Dummy 1")
        self.vbox.pack_start(b, True, True, 0)
        b = Gtk.Button("Dummy 2")
        self.vbox.pack_start(b, True, True, 0)

        self.top_container.pack_start(self.graphic_area, True, True, 0)
        self.top_container.pack_start(self.vbox, True, True, 0)
        self.top_container.show_all()


    def getWidget(self):
        return self.top_container

    def create_data(self, path):
        tmp_name = TMP_PATH + os.path.basename(path) + TMP_EXT
        p = Progress()
        CreateCache(path, tmp_name, p.get_progress())
        p.hide()
        f = open(tmp_name, 'rb')
        d = bytearray(f.read())
        f.close()

        # decimate date
        i = 0
        _len = len(d)
        samples = []
        offset = DECIMATE_FACTOR
        o = offset
        acc = 0
        max = 0
        while (i < _len):
            b = d[i]
            print(b)
            #b -= 128
            acc += b #(b * b)
            o -= 1
            if o <= 0:
                o = offset
                samples.append(acc)
                #print(acc)
                if acc > max:
                    max = acc
                acc = 0
            i += 1
        print("n samples = " + str(len(samples)))
        print ("SAMPLES_PER_SECOND = " + str(SAMPLES_PER_SECOND))

        ## normalize
        _len = len(samples)
        i = 0
        f = 1.0 / max
        print("max = " + str(max) + ", f = " + str(f))
        while (i < _len):
            samples[i] *= f
            i += 1
        self.data = samples




