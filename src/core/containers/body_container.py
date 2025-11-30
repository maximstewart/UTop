# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .left_container import LeftContainer
from .center_container import CenterContainer
from .right_container import RightContainer



class BodyContainer(Gtk.Box):
    def __init__(self):
        super(BodyContainer, self).__init__()

        self.ctx = self.get_style_context()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.ctx.add_class("body-container")

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...


    def _load_widgets(self):
        self.add(LeftContainer())
        self.add(CenterContainer())
        self.add(RightContainer())