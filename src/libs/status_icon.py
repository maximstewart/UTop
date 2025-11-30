# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import AppIndicator3

# Application imports



class StatusIcon():
    """ StatusIcon for Application to go to Status Tray. """

    def __init__(self):
        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        status_menu     = Gtk.Menu()
        icon_theme      = Gtk.IconTheme.get_default()
        check_menu_item = Gtk.CheckMenuItem.new_with_label("Update icon")
        quit_menu_item  = Gtk.MenuItem.new_with_label("Quit")

        # Create StatusNotifierItem
        self.indicator  = AppIndicator3.Indicator.new(
            f"{APP_NAME}-statusicon",
            "gtk-info",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        check_menu_item.connect("activate", self.check_menu_item_cb)
        quit_menu_item.connect("activate", self.quit_menu_item_cb)
        icon_theme.connect('changed', self.icon_theme_changed_cb)

        self.indicator.set_menu(status_menu)
        status_menu.append(check_menu_item)
        status_menu.append(quit_menu_item)
        status_menu.show_all()

    def update_icon(self, icon_name):
        self.indicator.set_icon(icon_name)

    def check_menu_item_cb(self, widget, data = None):
        icon_name = "parole" if widget.get_active() else "gtk-info"
        self.update_icon(icon_name)

    def icon_theme_changed_cb(self, theme):
        self.update_icon("gtk-info")

    def quit_menu_item_cb(self, widget, data = None):
        event_system.emit("tear-down")
