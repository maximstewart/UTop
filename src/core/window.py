# Python imports
import signal

# Lib imports
import gi
import cairo
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

# Application imports
from core.controllers.base_controller import BaseController



class ControllerStartExceptiom(Exception):
    ...



class Window(Gtk.ApplicationWindow):
    """ docstring for Window. """

    def __init__(self):
        super(Window, self).__init__()
        settings_manager.set_main_window(self)

        self._controller  = None
        self.guake_key    = settings_manager.get_guake_key()
        self.hidefunc     = None

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self._set_window_data()
        self._set_size_constraints()
        self._setup_window_toggle_event()

        self.show()


    def _setup_styling(self):
        self.set_title(f"{APP_NAME}")
        self.set_icon_from_file( settings_manager.get_window_icon() )

        self.set_default_size(128, 720)
        self.set_decorated(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_gravity(5)  # 5 = CENTER
        self.set_position(1) # 1 = CENTER, 4 = CENTER_ALWAYS

        self.set_keep_above(True)
        self.stick()

        ctx = self.get_style_context()
        ctx.add_class("main-window")
        ctx.add_class(f"mw_transparency_{settings.theming.transparency}")

    def _setup_signals(self):
        self.connect("focus-in-event", self._on_focus_in_event)
        self.connect("focus-out-event", self._on_focus_out_event)

        self.connect("delete-event", self.stop)
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, self.stop)

    def _subscribe_to_events(self):
        event_system.subscribe("tear-down", self.stop)
        event_system.subscribe("load-interactive-debug", self._load_interactive_debug)

    def _load_widgets(self):
        if settings_manager.is_debug():
            self.set_interactive_debugging(True)

        self._controller  = BaseController()
        if not self._controller:
            raise ControllerStartException("BaseController exited and doesn't exist...")

        self.add( self._controller.get_base_container() )

    def _display_manager(self):
        """ Try to detect which display manager we are running under... """

        import os
        if os.environ.get('WAYLAND_DISPLAY'):
            return 'WAYLAND'
    
        return 'X11'

    def _set_size_constraints(self):
        _min_width  = settings.config.main_window_min_width
        _min_height = settings.config.main_window_min_height
        _width      = settings.config.main_window_width
        _height     = settings.config.main_window_height

        self.set_size_request(_min_width, _min_height)
        self.set_default_size(_width, _height)

    def _set_window_data(self) -> None:
        screen = self.get_screen()
        visual = screen.get_rgba_visual()

        if visual and screen.is_composited() and settings.config.make_transparent == 0:
            self.set_visual(visual)
            self.set_app_paintable(True)
            # self.connect("draw", self._area_draw)

        # bind css file
        cssProvider  = Gtk.CssProvider()
        cssProvider.load_from_path( settings_manager.get_css_file() )
        screen       = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def _area_draw(self, widget: Gtk.ApplicationWindow, cr: cairo.Context) -> None:
        cr.set_source_rgba( *settings_manager.get_paint_bg_color() )
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)


    def _on_focus_in_event(self, widget, event):
        event_system.emit("pause-dnd-signals")

    def _on_focus_out_event(self, widget, event):
        event_system.emit("listen-dnd-signals")

    def _load_interactive_debug(self):
        self.set_interactive_debugging(True)

    def _setup_window_toggle_event(self) -> None:
        hidebound = None
        if not self.guake_key or not self._display_manager() == 'X11':
            return

        try:
            import gi
            gi.require_version('Keybinder', '3.0')
            from gi.repository import Keybinder

            Keybinder.init()
            Keybinder.set_use_cooked_accelerators(False)
        except (ImportError, ValueError) as e:
            logger.warning(e)
            logger.warning('Unable to load Keybinder module. This means the hide_window shortcut will be unavailable')

            return

        # Attempt to grab a global hotkey for hiding the window.
        # If we fail, we'll never hide the window, iconifying instead.
        try:
            hidebound = Keybinder.bind(self.guake_key, self._on_toggle_window, self)
        except (KeyError, NameError) as e:
            logger.warning(e)

        if not hidebound:
            logger.debug('Unable to bind hide_window key, another instance/window has it.')
            self.hidefunc = self.iconify
        else:
            self.hidefunc = self.hide

    def _on_toggle_window(self, data, window):
        """Handle a request to hide/show the window"""
        if not window.get_property('visible'):
            window.show()
            # Note: Needed to properly grab widget focus when set_skip_taskbar_hint set to True
            window.present()
            # NOTE:  Need here to enforce sticky after hide and reshow.
            window.stick()
        else:
            self.hidefunc()


    def start(self):
        Gtk.main()

    def stop(self, widget = None, eve = None):
        event_system.emit("shutting-down")

        size = self.get_size()
        pos  = self.get_position()

        settings_manager.set_main_window_width(size.width)
        settings_manager.set_main_window_height(size.height)
        settings_manager.set_main_window_x(pos.root_x)
        settings_manager.set_main_window_y(pos.root_y)
        settings_manager.save_settings()

        settings_manager.clear_pid()
        Gtk.main_quit()
