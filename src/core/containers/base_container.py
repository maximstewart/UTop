# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .header_container import HeaderContainer
from .body_container import BodyContainer
from .footer_container import FooterContainer



class BaseContainer(Gtk.Box):
    def __init__(self):
        super(BaseContainer, self).__init__()

        self.ctx = self.get_style_context()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.ctx.add_class("base-container")

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        self.add(HeaderContainer())
        self.add(BodyContainer())
        self.add(FooterContainer())
