# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..widgets.category_list_widget import CategoryListWidget



class LeftContainer(Gtk.Box):
    def __init__(self):
        super(LeftContainer, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.VERTICAL)

        self.set_vexpand(True)

        ctx = self.get_style_context()
        ctx.add_class("left-container")

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        self.add(CategoryListWidget())
