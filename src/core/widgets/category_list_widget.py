# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from xdg.DesktopEntry import DesktopEntry

# Application imports
from libs.desktop_parsing.app_finder import find_apps




class CategoryListWidget(Gtk.ButtonBox):
    def __init__(self):
        super(CategoryListWidget, self).__init__()

        self.ctx                  = self.get_style_context()
        self.active_category: str = 'Accessories'

        self.category_dict: {} = {
            "Accessories": [],
            "Multimedia":  [],
            "Graphics":    [],
            "Game":        [],
            "Office":      [],
            "Development": [],
            "Internet":    [],
            "Settings":    [],
            "System":      [],
            "Wine":        [],
            "Other":       []
        }

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()
        self.fill_menu_objects()

        self.show_all()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.ctx.add_class("category-list-widget")

    def _setup_signals(self):
        event_system.subscribe("refresh-active-category", self.refresh_active_category)

    def _subscribe_to_events(self):
        ...


    def _load_widgets(self):
        for category in self.category_dict.keys():
            button = Gtk.Button(label = category)
            button.connect("clicked", self.set_active_category)
            button.show()

            self.add(button)

    def set_active_category(self, button):
        self.active_category = button.get_label()
        event_system.emit(
            "load-active-category",
            (self.category_dict[ self.active_category ],)
        )

    def fill_menu_objects(self, apps: [] = []):
        if not apps:
            apps = find_apps()

        for app in apps:
            fPath    = app.get_filename()
            xdgObj   = DesktopEntry( fPath )

            title    = xdgObj.getName()
            groups   = xdgObj.getCategories()
            comment  = xdgObj.getComment()
            icon     = xdgObj.getIcon()
            mainExec = xdgObj.getExec()
            tryExec  = xdgObj.getTryExec()

            group    = ""
            if "Accessories" in groups or "Utility" in groups:
                group = "Accessories"
            elif "Multimedia" in groups or "Video" in groups or "Audio" in groups:
                group = "Multimedia"
            elif "Development" in groups:
                group = "Development"
            elif "Game" in groups:
                group = "Game"
            elif "Internet" in groups or "Network" in groups:
                group = "Internet"
            elif "Graphics" in groups:
                group = "Graphics"
            elif "Office" in groups:
                group = "Office"
            elif "System" in groups:
                group = "System"
            elif "Settings" in groups:
                group = "Settings"
            elif "Wine" in groups:
                group = "Wine"
            else:
                group = "Other"

            self.category_dict[group].append(
                {
                    "title":  title,
                    "groups": groups,
                    "comment": comment,
                    "exec": mainExec,
                    "tryExec": tryExec,
                    "fileName": fPath.split("/")[-1],
                    "filePath": fPath,
                    "icon": icon
                }
            )

    def refresh_active_category(self):
        event_system.emit(
            "load-active-category",
            (self.category_dict[ self.active_category ],)
        )

