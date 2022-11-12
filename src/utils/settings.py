# Python imports
import os
import json
import inspect

# Gtk imports

# Application imports
from .logger import Logger




class Settings:
    def __init__(self):
        self._SCRIPT_PTH    = os.path.dirname(os.path.realpath(__file__))
        self._USER_HOME     = os.path.expanduser('~')
        self._CONFIG_PATH   = f"{self._USER_HOME}/.config/{app_name.lower()}"
        self._PLUGINS_PATH  = f"{self._CONFIG_PATH}/plugins"
        self._GLADE_FILE    = f"{self._CONFIG_PATH}/Main_Window.glade"
        self._KEY_BINDINGS_FILE  = f"{self._CONFIG_PATH}/key-bindings.json"
        self._CSS_FILE      = f"{self._CONFIG_PATH}/stylesheet.css"
        self._DEFAULT_ICONS = f"{self._CONFIG_PATH}/icons"
        self._PID_FILE      = f"{self._CONFIG_PATH}/{app_name.lower()}.pid"
        self._WINDOW_ICON   = f"{self._DEFAULT_ICONS}/{app_name.lower()}.png"
        self._USR_PATH      = f"/usr/share/{app_name.lower()}"

        if not os.path.exists(self._CONFIG_PATH):
            os.mkdir(self._CONFIG_PATH)
        if not os.path.exists(self._PLUGINS_PATH):
            os.mkdir(self._PLUGINS_PATH)

        if not os.path.exists(self._GLADE_FILE):
            self._GLADE_FILE   = f"{self._USR_PATH}/Main_Window.glade"
        if not os.path.exists(self._KEY_BINDINGS_FILE):
            self._KEY_BINDINGS_FILE  = f"{self._USR_PATH}/key-bindings.json"
        if not os.path.exists(self._CSS_FILE):
            self._CSS_FILE     = f"{self._USR_PATH}/stylesheet.css"
        if not os.path.exists(self._WINDOW_ICON):
            self._WINDOW_ICON  = f"{self._USR_PATH}/icons/{app_name.lower()}.png"
        if not os.path.exists(self._DEFAULT_ICONS):
            self.DEFAULT_ICONS = f"{self._USR_PATH}/icons"

        # '_filters'
        self._office_filter = ('.doc', '.docx', '.xls', '.xlsx', '.xlt', '.xltx', '.xlm', '.ppt', 'pptx', '.pps', '.ppsx', '.odt', '.rtf')
        self._vids_filter   = ('.mkv', '.avi', '.flv', '.mov', '.m4v', '.mpg', '.wmv', '.mpeg', '.mp4', '.webm')
        self._txt_filter    = ('.txt', '.text', '.sh', '.cfg', '.conf')
        self._music_filter  = ('.psf', '.mp3', '.ogg' , '.flac')
        self._images_filter = ('.png', '.jpg', '.jpeg', '.gif', '.ico', '.tga')
        self._pdf_filter    = ('.pdf')

        self._success_color = "#88cc27"
        self._warning_color = "#ffa800"
        self._error_color   = "#ff0000"

        with open(self._KEY_BINDINGS_FILE) as file:
            bindings = json.load(file)["keybindings"]
            keybindings.configure(bindings)

        self._guake_key     = bindings["guake_key"]

        self._builder       = None
        self._logger        = Logger(self._CONFIG_PATH).get_logger()

        self._trace_debug   = False
        self._debug         = False
        self._dirty_start   = False


    def do_dirty_start_check(self):
        if not os.path.exists(self._PID_FILE):
            self._write_new_pid()
        else:
            with open(self._PID_FILE, "r") as _pid:
                pid = _pid.readline().strip()
                if pid not in ("", None):
                    self._check_alive_status(int(pid))
                else:
                    self._write_new_pid()

    """ Check For the existence of a unix pid. """
    def _check_alive_status(self, pid):
        print(f"PID Found: {pid}")
        try:
            os.kill(pid, 0)
        except OSError:
            print(f"{app_name} is starting dirty...")
            self._dirty_start = True
            self._write_new_pid()
            return

        print("PID is alive... Let downstream errors (sans debug args) handle app closure propigation.")

    def _write_new_pid(self):
        pid = os.getpid()
        self._write_pid(pid)

    def _clean_pid(self):
        os.unlink(self._PID_FILE)

    def _write_pid(self, pid):
        with open(self._PID_FILE, "w") as _pid:
            _pid.write(f"{pid}")

    def register_signals_to_builder(self, classes=None):
        handlers = {}

        for c in classes:
            methods = None
            try:
                methods = inspect.getmembers(c, predicate=inspect.ismethod)
                handlers.update(methods)
            except Exception as e:
                print(repr(e))

        self._builder.connect_signals(handlers)


    def set_builder(self, builder) -> any:  self._builder = builder
    def get_builder(self)          -> any:  return self._builder
    def get_glade_file(self)       -> str:  return self._GLADE_FILE

    def get_logger(self)        -> Logger:  return self._logger
    def get_plugins_path(self)  -> str:     return self._PLUGINS_PATH
    def get_icon_theme(self)    -> str:     return self._ICON_THEME
    def get_css_file(self)      -> str:     return self._CSS_FILE
    def get_window_icon(self)   -> str:     return self._WINDOW_ICON
    def get_home_path(self)     -> str:     return self._USER_HOME

    # Filter returns
    def get_office_filter(self) -> tuple: return self._office_filter
    def get_vids_filter(self)   -> tuple: return self._vids_filter
    def get_text_filter(self)   -> tuple: return self._txt_filter
    def get_music_filter(self)  -> tuple: return self._music_filter
    def get_images_filter(self) -> tuple: return self._images_filter
    def get_pdf_filter(self)    -> tuple: return self._pdf_filter
    def get_guake_key(self)     -> tuple: return self._guake_key

    def get_success_color(self) -> str:   return self._success_color
    def get_warning_color(self) -> str:   return self._warning_color
    def get_error_color(self)   -> str:   return self._error_color

    def is_trace_debug(self)    -> str:   return self._trace_debug
    def is_debug(self)          -> str:   return self._debug
    def is_dirty_start(self)    -> bool:  return self._dirty_start
    def clear_pid(self): self._clean_pid()

    def set_trace_debug(self, trace_debug):
        self._trace_debug = trace_debug

    def set_debug(self, debug):
        self._debug = debug
