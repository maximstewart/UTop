# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..widgets.search_command_widget import SearchCommandWidget
from ..widgets.tab_widget import TabWidget



class CenterContainer(Gtk.Box):
    def __init__(self):
        super(CenterContainer, self).__init__()

        self._builder = settings_manager.get_builder()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.VERTICAL)

        self.set_hexpand(True)
        self.set_vexpand(True)

        ctx = self.get_style_context()
        ctx.add_class("center-container")

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        self.add(SearchCommandWidget())
        self.add(TabWidget())
