# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..widgets.clock_widget import ClockWidget



class FooterContainer(Gtk.Box):
    def __init__(self):
        super(FooterContainer, self).__init__()

        self.ctx = self.get_style_context()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.set_hexpand(True)

        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.ctx.add_class("footer-container")

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...


    def _load_widgets(self):
        # self.add(ClockWidget())
        self.pack_end(ClockWidget(), False, False, 5)
