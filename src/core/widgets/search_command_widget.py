# Python imports
import subprocess

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

# Application imports



class SearchCommandWidget(Gtk.SearchEntry):
    def __init__(self):
        super(SearchCommandWidget, self).__init__()

        self.mode       = ""
        self.timeout_id = None

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.set_placeholder_text("Apps /a | Search /s | Command /c ...")

    def _setup_signals(self):
        self.connect("search-changed", self._search_changed)
        self.connect("activate", self._handle_enter)

    def _subscribe_to_events(self):
        event_system.subscribe("focus-search", self._focus_search)
    
    def _load_widgets(self):
        ...

    def _focus_search(self):
        self.grab_focus()

    def _search_changed(self, widget):
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None

        entry = widget.get_text().strip()
        if not entry or len(entry) <= 3:
            self.mode       = ""
            self.request    = ""

            event_system.emit("refresh-active-category")
            return

        self.mode       = entry[0:2]
        self.request    = entry[2:].strip()
        self.timeout_id = GLib.timeout_add(600, self._match_mode)

    def _match_mode(self):
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None

        match self.mode:
            case "/a":
                self.query_all_categories()
            case "/s":
                sub_mode = self.request[0:2]
                match sub_mode:
                    case "/f ":
                        ...
                    case "/d":
                        ...
                    case _:
                        ...
                ...
            case _:
                ...

    def _handle_enter(self, widget):
        if self.mode != "/c": return

        subprocess.Popen(
            self.request.split(),
            start_new_session = True,
            stdout = None,
            stderr = None
        )

    def query_all_categories(self):
        event_system.emit("query-all-categories", (self.request,))
