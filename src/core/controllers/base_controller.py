# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from libs.mixins.ipc_signals_mixin import IPCSignalsMixin
from libs.mixins.keyboard_signals_mixin import KeyboardSignalsMixin

from ..containers.base_container import BaseContainer

from .base_controller_data import BaseControllerData
from .bridge_controller import BridgeController



class BaseController(IPCSignalsMixin, KeyboardSignalsMixin, BaseControllerData):
    """ docstring for BaseController. """

    def __init__(self):

        self._setup_controller_data()
        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_controllers()
        self._load_plugins_and_files()

        logger.info(f"Made it past {self.__class__} loading...")
        settings_manager.set_end_load_time()
        settings_manager.log_load_time()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        self.window.connect("focus-out-event", self.unset_keys_and_data)
        self.window.connect("key-press-event", self.on_global_key_press_controller)
        self.window.connect("key-release-event", self.on_global_key_release_controller)

    def _subscribe_to_events(self):
        event_system.subscribe("shutting-down", lambda: print("Shutting down..."))
        event_system.subscribe("handle-file-from-ipc", self.handle_file_from_ipc)
        event_system.subscribe("handle-dir-from-ipc", self.handle_dir_from_ipc)
        event_system.subscribe("tggl-top-main-menubar", self._tggl_top_main_menubar)

    def _load_controllers(self):
        BridgeController()

    def _load_plugins_and_files(self):
        args, unknownargs = settings_manager.get_starting_args()
        if args.no_plugins == "false":
            self.plugins_controller.pre_launch_plugins()
            self.plugins_controller.post_launch_plugins()

        for file in settings_manager.get_starting_files():
            event_system.emit("post-file-to-ipc", file)

    def _tggl_top_main_menubar(self):
        logger.debug("_tggl_top_main_menubar > stub...")

    def _load_glade_file(self):
        self.builder.add_from_file( settings_manager.get_glade_file() )
        self.builder.expose_object("main_window", self.window)

        settings_manager.set_builder(self.builder)
        self.base_container = BaseContainer()

        settings_manager.register_signals_to_builder([self, self.base_container])