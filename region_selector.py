import cairo
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk


class RegionWindow(Gtk.ApplicationWindow):
  rectangle_start = (0,0)
  rectangle_end= (0,0)

  def __init__(self, app):
    # instantiate
    self.box = Gtk.Box()
    self.d = Gtk.DrawingArea()
    self.box.pack_start(self.d, True, True, 0)
    self.d.set_size_request(500, 500)

    # decoration
    Gtk.ApplicationWindow.__init__(self, application = app)
    self.set_border_width(0)
    self.set_app_paintable(True)
    self.set_decorated(False)
    self.set_property("skip-taskbar-hint", True)
    self.set_keep_above(True)
    self.connect("draw", self.draw)

    # register cbs
    self.connect("button-press-event", self.mouse_press)
    self.connect("button-release-event", self.mouse_release)
    self.connect("motion-notify-event", self.motion_notify)

    # size/color
    #display = Gdk.Display.get_default()
    #screen = display.get_screen(0) # XXX
    screen = self.get_screen()
    visual = screen.get_rgba_visual()
    if visual and screen.is_composited():
      self.set_visual(visual)

    width = screen.width()
    height = screen.height()
    self.move(0,0)
    #self.resize(width, height)
    self.fullscreen()

    # show
    self.add(self.box)
    self.show_all()
  
  def motion_notify(self, widget, context):
    self.rectangle_end = (context.x, context.y)
    if self.rectangle_start == self.rectangle_end:
      return
    widget.queue_draw()
  
  def mouse_press(self, widget, context):
    self.rectangle_start = (context.x, context.y)
    self.rectangle_end = (context.x, context.y)
    widget.queue_draw()

  def mouse_release(self, widget, context):
    self.rectangle_end = (context.x, context.y)
    widget.queue_draw()
  
  def draw(self, widget, context):
    context.set_source_rgba(0, 0, 0, 0.5)
    context.set_operator(cairo.OPERATOR_SOURCE)
    context.paint()
    context.set_operator(cairo.OPERATOR_OVER)

    print((self.rectangle_start[0], self.rectangle_start[1], self.rectangle_end[0], self.rectangle_end[1]))
    context.set_line_width(1)
    context.set_source_rgb(1.0, 1.0, 1.0)
    context.rectangle(self.rectangle_start[0], self.rectangle_start[1], self.rectangle_end[0] - self.rectangle_start[0], self.rectangle_end[1] - self.rectangle_start[1])
    context.stroke()


class RegionSelector(Gtk.Application):
  def __init__(self):
    Gtk.Application.__init__(self, application_id = "github.com.rita-rita-ritan.AutoScreenCapture")

  def do_activate(self):
    RegionWindow(self)

app = RegionSelector()
app.run()
