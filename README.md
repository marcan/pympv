pympv
=====
A python wrapper for libmpv.

#### Basic usage
```python
import sys
import mpv

def main(args):
    if len(args) != 1:
        print('pass a single media file as argument')
        return 1

    try:
        m = mpv.Context()
    except mpv.MPVError:
        print('failed creating context')
        return 1

    m.set_option('input-default-bindings')
    m.set_option('osc')
    m.set_option('input-vo-keyboard')
    m.initialize()

    m.command('loadfile', args[0])

    while True:
        event = m.wait_event(.01)
        if event.id == mpv.Events.none:
            continue
        print(event.name)
        if event.id in [mpv.Events.end_file, mpv.Events.shutdown]:
            break

if __name__ == '__main__':
    try:
        exit(main(sys.argv[1:]) or 0)
    except mpv.MPVError as e:
        print(str(e))
        exit(1)
```

#### PyGObject usage
```python
#!/usr/bin/env python3
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
```

libmpv is a client library for the media player mpv

For more info see: https://github.com/mpv-player/mpv/blob/master/libmpv/client.h

pympv was originally written by Andre D, and the PyPI package is maintained
by Hector Martin.
