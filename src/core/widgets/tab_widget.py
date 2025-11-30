# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..widgets.category_widget import CategoryWidget
from ..widgets.vte_widget import VteWidget



class TabWidget(Gtk.Notebook):
    def __init__(self):
        super(TabWidget, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.set_hexpand(True)
        self.set_vexpand(True)

        ctx = self.get_style_context()
        ctx.add_class("tab-widget")

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("focus-apps", self.focus_apps)
        event_system.subscribe("focus-terminal", self.focus_terminal)

    def _load_widgets(self):
        scroll_view = Gtk.ScrolledWindow()
        viewport    = Gtk.Viewport()

        viewport.add(CategoryWidget())
        scroll_view.add(viewport)

        scroll_view.show_all()

        self.insert_page(scroll_view, Gtk.Label(label = "Apps"), 0)
        self.insert_page(VteWidget(), Gtk.Label(label = "Terminal"), 1)

        self.set_current_page(0)

    def focus_apps(self):
        widget = self.get_nth_page(0).get_children()[0].get_children()[0]
        self.set_current_page(0)
        widget.grab_focus()

    def focus_terminal(self):
        widget = self.get_nth_page(1)
        self.set_current_page(1)
        widget.grab_focus()
