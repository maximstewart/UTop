# Python imports
import inspect
import time
import json
import zipfile

from os import path
from os import mkdir

# Lib imports

# Application imports
from ..singleton import Singleton
from .start_check_mixin import StartCheckMixin
from .options.settings import Settings



class MissingConfigError(Exception):
    pass



class SettingsManager(StartCheckMixin, Singleton):
    def __init__(self):
        self._SCRIPT_PTH: str        = path.dirname(path.realpath(__file__))
        self._USER_HOME: str         = path.expanduser('~')
        self._HOME_CONFIG_PATH: str  = f"{self._USER_HOME}/.config/{APP_NAME.lower()}"
        self._USR_PATH: str          = f"/usr/share/{APP_NAME.lower()}"
        self._USR_CONFIG_FILE: str   = f"{self._USR_PATH}/settings.json"

        self._CONTEXT_PATH: str      = f"{self._HOME_CONFIG_PATH}/context_path"
        self._PLUGINS_PATH: str      = f"{self._HOME_CONFIG_PATH}/plugins"
        self._DEFAULT_ICONS: str     = f"{self._HOME_CONFIG_PATH}/icons"
        self._CONFIG_FILE: str       = f"{self._HOME_CONFIG_PATH}/settings.json"
        self._GLADE_FILE: str        = f"{self._HOME_CONFIG_PATH}/Main_Window.glade"
        self._CSS_FILE: str          = f"{self._HOME_CONFIG_PATH}/stylesheet.css"
        self._KEY_BINDINGS_FILE: str = f"{self._HOME_CONFIG_PATH}/key-bindings.json"
        self._PID_FILE: str          = f"{self._HOME_CONFIG_PATH}/{APP_NAME.lower()}.pid"
        self._UI_WIDEGTS_PATH: str   = f"{self._HOME_CONFIG_PATH}/ui_widgets"
        self._CONTEXT_MENU: str      = f"{self._HOME_CONFIG_PATH}/contexct_menu.json"
        self._WINDOW_ICON: str       = f"{self._DEFAULT_ICONS}/{APP_NAME.lower()}.png"

        # self._USR_CONFIG_FILE: str   = f"{self._USR_PATH}/settings.json"
        # self._PLUGINS_PATH: str      = f"plugins"
        # self._CONFIG_FILE: str       = f"settings.json"
        # self._GLADE_FILE: str        = f"Main_Window.glade"
        # self._CSS_FILE: str          = f"stylesheet.css"
        # self._KEY_BINDINGS_FILE: str = f"key-bindings.json"
        # self._PID_FILE: str          = f"{APP_NAME.lower()}.pid"
        # self._WINDOW_ICON: str       = f"{APP_NAME.lower()}.png"
        # self._UI_WIDEGTS_PATH: str   = f"ui_widgets"
        # self._CONTEXT_MENU: str      = f"contexct_menu.json"
        # self._DEFAULT_ICONS: str     = f"icons"


        # with zipfile.ZipFile("files.zip", mode="r", allowZip64=True) as zf:
        #     with io.TextIOWrapper(zf.open("text1.txt"), encoding="utf-8") as f:


        if not path.exists(self._HOME_CONFIG_PATH):
            mkdir(self._HOME_CONFIG_PATH)
        if not path.exists(self._PLUGINS_PATH):
            mkdir(self._PLUGINS_PATH)

        if not path.exists(self._DEFAULT_ICONS):
            self._DEFAULT_ICONS = f"{self._USR_PATH}/icons"
            if not path.exists(self._DEFAULT_ICONS):
                raise MissingConfigError("Unable to find the application icons directory.")
        if not path.exists(self._GLADE_FILE):
            self._GLADE_FILE   = f"{self._USR_PATH}/Main_Window.glade"
            if not path.exists(self._GLADE_FILE):
                raise MissingConfigError("Unable to find the application Glade file.")
        if not path.exists(self._KEY_BINDINGS_FILE):
            self._KEY_BINDINGS_FILE = f"{self._USR_PATH}/key-bindings.json"
            if not path.exists(self._KEY_BINDINGS_FILE):
                raise MissingConfigError("Unable to find the application Keybindings file.")
        if not path.exists(self._CSS_FILE):
            self._CSS_FILE     = f"{self._USR_PATH}/stylesheet.css"
            if not path.exists(self._CSS_FILE):
                raise MissingConfigError("Unable to find the application Stylesheet file.")
        if not path.exists(self._WINDOW_ICON):
            self._WINDOW_ICON  = f"{self._USR_PATH}/icons/{APP_NAME.lower()}.png"
            if not path.exists(self._WINDOW_ICON):
                raise MissingConfigError("Unable to find the application icon.")
        if not path.exists(self._UI_WIDEGTS_PATH):
            self._UI_WIDEGTS_PATH  = f"{self._USR_PATH}/ui_widgets"
        if not path.exists(self._CONTEXT_MENU):
            self._CONTEXT_MENU  = f"{self._USR_PATH}/contexct_menu.json"


        try:
            with open(self._KEY_BINDINGS_FILE) as file:
                bindings        = json.load(file)["keybindings"]
                self._guake_key = bindings["guake_key"]
                keybindings.configure(bindings)
        except Exception as e:
            print( f"Settings Manager: {self._KEY_BINDINGS_FILE}\n\t\t{repr(e)}" )

        try:
            with open(self._CONTEXT_MENU) as file:
                self._context_menu_data = json.load(file)
        except Exception as e:
            print( f"Settings Manager: {self._CONTEXT_MENU}\n\t\t{repr(e)}" )


        self.settings: Settings    = None
        self._main_window          = None
        self._builder              = None
        self.PAINT_BG_COLOR: tuple = (0, 0, 0, 0.0)

        self._trace_debug: bool    = False
        self._debug: bool          = False
        self._dirty_start: bool    = False
        self._passed_in_file: bool = False
        self._starting_files: list = []


    def register_signals_to_builder(self, classes = None):
        handlers = {}

        for c in classes:
            methods = None
            try:
                methods = inspect.getmembers(c, predicate = inspect.ismethod)
                handlers.update(methods)
            except Exception as e:
                ...

        self._builder.connect_signals(handlers)

    def set_main_window(self, window): self._main_window  = window
    def set_builder(self, builder) -> any:  self._builder = builder

    def get_monitor_data(self) -> list:
        screen = self._main_window.get_screen()
        monitors = []
        for m in range(screen.get_n_monitors()):
            monitors.append(screen.get_monitor_geometry(m))
            print("{}x{}+{}+{}".format(monitor.width, monitor.height, monitor.x, monitor.y))

        return monitors

    def get_main_window(self)        -> any: return self._main_window
    def get_builder(self)            -> any: return self._builder
    def get_paint_bg_color(self)     -> any: return self.PAINT_BG_COLOR
    def get_glade_file(self)         -> str: return self._GLADE_FILE
    def get_ui_widgets_path(self)    -> str: return self._UI_WIDEGTS_PATH
    def get_context_menu_data(self)  -> str: return self._context_menu_data

    def get_context_path(self)     -> str:   return self._CONTEXT_PATH
    def get_plugins_path(self)     -> str:   return self._PLUGINS_PATH
    def get_icon_theme(self)       -> str:   return self._ICON_THEME
    def get_css_file(self)         -> str:   return self._CSS_FILE
    def get_home_config_path(self) -> str:   return self._HOME_CONFIG_PATH
    def get_window_icon(self)      -> str:   return self._WINDOW_ICON
    def get_home_path(self)        -> str:   return self._USER_HOME
    def get_starting_files(self)   -> list:  return self._starting_files
    def get_guake_key(self)        -> tuple: return self._guake_key

    def get_starting_args(self):
        return self.args, self.unknownargs

    def set_main_window_x(self, x: int = 0):                 self.settings.config.main_window_x  = x
    def set_main_window_y(self, y: int = 0):                 self.settings.config.main_window_y  = y
    def set_main_window_width(self, width: int = 800):       self.settings.config.main_window_width  = width
    def set_main_window_height(self, height: int = 600):     self.settings.config.main_window_height = height
    def set_main_window_min_width(self, width: int = 720):   self.settings.config.main_window_min_width  = width
    def set_main_window_min_height(self, height: int = 480): self.settings.config.main_window_min_height = height
    def set_starting_files(self, files: list):               self._starting_files = files
    def set_start_load_time(self): self._start_load_time = time.perf_counter()
    def set_end_load_time(self):   self._end_load_time   = time.perf_counter()

    def set_starting_args(self, args, unknownargs):
        self.args = args
        self.unknownargs = unknownargs

    def set_trace_debug(self, trace_debug: bool):
        self._trace_debug = trace_debug

    def set_debug(self, debug: bool):
        self._debug = debug

    def set_is_starting_with_file(self, is_passed_in_file: bool = False):
        self._passed_in_file = is_passed_in_file

    def is_trace_debug(self)       -> str:   return self._trace_debug
    def is_debug(self)             -> str:   return self._debug
    def is_starting_with_file(self) -> bool: return self._passed_in_file

    def log_load_time(self):       logger.info( f"Load Time: {self._end_load_time - self._start_load_time}" )

    def call_method(self, target_class: any = None, _method_name: str = "", data: any = None):
        method_name = str(_method_name)
        method      = getattr(target_class, method_name, lambda data: f"No valid key passed...\nkey={method_name}\nargs={data}")
        return method(data) if data else method()

    def load_settings(self):
        if not path.exists(self._CONFIG_FILE):
            self.settings = Settings()
            return

        with open(self._CONFIG_FILE) as file:
            data          = json.load(file)
            data["load_defaults"] = False
            self.settings = Settings(**data)

    def save_settings(self):
        with open(self._CONFIG_FILE, 'w') as outfile:
            json.dump(self.settings.as_dict(), outfile, separators=(',', ':'), indent=4)