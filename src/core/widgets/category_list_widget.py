# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gio

from xdg.DesktopEntry import DesktopEntry

# Application imports
from libs.desktop_parsing.app_finder import find_apps




class CategoryListWidget(Gtk.ButtonBox):
    def __init__(self):
        super(CategoryListWidget, self).__init__()

        self.active_category   = None
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

        self.dir_watchers: []  = []

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()
        self._fill_menu_objects()

        self.show_all()


    def _setup_styling(self):
        self.set_orientation(Gtk.Orientation.VERTICAL)
        ctx = self.get_style_context()
        ctx.add_class("category-list-widget")

    def _setup_signals(self):
        self._load_dir_watchers()

    def _subscribe_to_events(self):
        event_system.subscribe("get-active-category", self.get_active_category)
        event_system.subscribe("refresh-active-category", self.refresh_active_category)
        event_system.subscribe("query-all-categories", self.query_all_categories)

    def _load_widgets(self):
        for category in self.category_dict.keys():
            button = Gtk.Button(label = category)
            button.connect("clicked", self._set_active_category)
            button.show()

            self.add(button)

            if category == "Accessories":
                self.active_category = button
                self.active_category.get_style_context().add_class("active-category")

        self.category_dict["All"] = []

    def _reset_dir_watchers(self):
        self._clear_dir_watchers()
        self._load_dir_watchers()

    def _load_dir_watchers(self):
        for dpath in settings_manager.settings.config.application_dirs:
            dir_watcher  = Gio.File.new_for_path(dpath).monitor_directory(
                                Gio.FileMonitorFlags.WATCH_MOVES,
                                Gio.Cancellable()
                            )

            watch_id = dir_watcher.connect(
                "changed",
                self._dir_watch_updates
            )

            dir_watcher.watch_id = watch_id
            self.dir_watchers.append(dir_watcher)

    def _clear_dir_watchers(self):
        for watcher in self.dir_watchers:
            watcher.cancel()
            watcher.disconnect(watcher.watch_id)
            watcher.run_dispose()

        self.dir_watchers.clear()

    def _dir_watch_updates(self, file_monitor, file, other_file = None, eve_type = None):
        if eve_type in  [Gio.FileMonitorEvent.CREATED, Gio.FileMonitorEvent.DELETED,
                        Gio.FileMonitorEvent.RENAMED, Gio.FileMonitorEvent.MOVED_IN,
                        Gio.FileMonitorEvent.MOVED_OUT]:

            GLib.idle_add(self._reload_meu)

    def _reload_meu(self):
        for category in self.category_dict:
            self.category_dict[category].clear()

        self._fill_menu_objects()
        event_system.emit(
            "load-active-category",
            (self.category_dict[ self.active_category.get_label() ],)
        )

    def _fill_menu_objects(self, apps: [] = []):
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

            entry = {
                "title":  title,
                "groups": groups,
                "comment": comment,
                "exec": mainExec,
                "tryExec": tryExec,
                "fileName": fPath.split("/")[-1],
                "filePath": fPath,
                "icon": icon
            }

            self.category_dict["All"].append(entry)
            self.category_dict[group].append(entry)

    def _set_active_category(self, button):
        self.active_category.get_style_context().remove_class("active-category")
        self.active_category = button
        self.active_category.get_style_context().add_class("active-category")

        event_system.emit(
            "load-active-category",
            (self.category_dict[ self.active_category.get_label() ],)
        )

    def query_all_categories(self, query: str):
        self.active_category.get_style_context().remove_class("active-category")

        filtered_group = []
        for app in self.category_dict["All"]:
            if (
                query in app["title"].lower()or \
                query in app["comment"].lower()
            ):
                filtered_group.append(app)

        event_system.emit("load-active-category", (filtered_group,))

    def get_active_category(self):
        return self.active_category

    def refresh_active_category(self):
        self.active_category.get_style_context().add_class("active-category")
        event_system.emit(
            "load-active-category",
            (self.category_dict[ self.active_category.get_label() ],)
        )
