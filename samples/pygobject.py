#!/usr/bin/env python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ctypes
import sys
from ctypes import CFUNCTYPE, c_char_p, c_void_p

import gi
import mpv

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from OpenGL import GL, GLX


class MainClass(Gtk.Window):

    def __init__(self, media):
        super(MainClass, self).__init__()
        self.media = media
        self.set_default_size(600, 400)
        self.connect("destroy", self.on_destroy)

        frame = Gtk.Frame()
        self.area = OpenGlArea()
        self.area.connect("realize", self.play)
        frame.add(self.area)
        self.add(frame)
        self.show_all()

    def on_destroy(self, widget, data=None):
        Gtk.main_quit()

    def play(self, arg1):
        self.area.play(self.media)


class OpenGlArea(Gtk.GLArea):

    def __init__(self, **properties):
        super().__init__(**properties)

        self.gl_context: mpv.OpenGLRenderContext = None

        try:
            self.mpv = mpv.Context()
            self.mpv.initialize()
        except mpv.MPVError:
            raise RuntimeError('failed creating context')

        # self.mpv.set_property("gpu-context", "wayland")
        self.mpv.set_property("terminal", True)

        self.connect("realize", self.on_realize)
        self.connect("render", self.on_render)
        self.connect("unrealize", self.on_unrealize)

    # noinspection PyUnusedLocal
    def on_realize(self, area: Gtk.GLArea):
        self.make_current()
        self.gl_context = mpv.OpenGLRenderContext(self.mpv, get_process_address)
        self.gl_context.set_update_callback(self.queue_render)

    def on_unrealize(self, arg):
        if self.gl_context:
            self.gl_context.close()
        self.mpv.shutdown()

    def on_render(self, arg1, arg2):
        factor = self.get_scale_factor()
        rect: Gdk.Rectangle = self.get_allocated_size()[0]

        if self.gl_context:
            fbo = {
                "fbo": GL.glGetIntegerv(GL.GL_DRAW_FRAMEBUFFER_BINDING),
                "w": rect.width * factor,
                "h": rect.height * factor,
            }
            self.gl_context.render(opengl_fbo=fbo, flip_y=True)

        return True

    def play(self, media):
        self.mpv.command('loadfile', media)


@CFUNCTYPE(c_void_p, c_char_p)
def get_process_address(name):
    address = GLX.glXGetProcAddress(name.decode("utf-8"))
    return ctypes.cast(address, ctypes.c_void_p).value


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) == 1:
        import locale

        locale.setlocale(locale.LC_NUMERIC, 'C')

        application = MainClass(args[0])
        Gtk.main()
    else:
        print('pass a single media file as argument and try again')
