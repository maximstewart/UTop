# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..widgets.pager_widget import PagerWidget




class HeaderContainer(Gtk.ButtonBox):
    def __init__(self):
        super(HeaderContainer, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.set_hexpand(True)
        self.set_vexpand(True)

        self.set_orientation(Gtk.Orientation.HORIZONTAL)

        ctx = self.get_style_context()
        ctx.add_class("header-container")

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        pager_widget = PagerWidget().get_widget()

        pager_widget.show()

        self.add(pager_widget)
