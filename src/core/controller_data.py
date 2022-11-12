# Python imports
import os

# Lib imports
import gi
from gi.repository import GObject

# Application imports
from plugins.plugins_controller import PluginsController




try:
    from gi.repository import GdkX11
except ImportError:
    logger.debug("Could not import X11 gir module...")

def display_manager():
    """ Try to detect which display manager we are running under... """
    if os.environ.get('WAYLAND_DISPLAY'):
        return 'WAYLAND'
    return 'X11'  # Fallback assumption of X11


if display_manager() == 'X11':
    try:
        gi.require_version('Keybinder', '3.0')
        from gi.repository import Keybinder
        Keybinder.init()
        Keybinder.set_use_cooked_accelerators(False)
    except (ImportError, ValueError):
        logger.debug('Unable to load Keybinder module. This means the hide_window shortcut will be unavailable')




class ControllerData:
    ''' ControllerData contains most of the state of the app at ay given time. It also has some support methods. '''

    def setup_controller_data(self) -> None:
        self.builder       = None
        self.core_widget   = None

        self.load_glade_file()
        self.plugins       = PluginsController()

        self.hidefunc      = None
        self.show_image    = True
        self.guake_key     = settings.get_guake_key()


    def setup_toggle_event(self) -> None:
        self.window = settings.get_builder().get_object(f"{app_name.lower()}")

        # Attempt to grab a global hotkey for hiding the window.
        # If we fail, we'll never hide the window, iconifying instead.
        if self.guake_key and display_manager() == 'X11':
            try:
                hidebound = Keybinder.bind(self.guake_key, self.on_hide_window)
            except (KeyError, NameError):
                pass

            if not hidebound:
                logger.debug('Unable to bind hide_window key, another instance/window has it.')
                self.hidefunc = self.window.iconify
            else:
                self.hidefunc = self.window.hide


    def clear_console(self) -> None:
        ''' Clears the terminal screen. '''
        os.system('cls' if os.name == 'nt' else 'clear')

    def call_method(self, _method_name: str, data: type) -> type:
        '''
            Calls a method from scope of class.

                    Parameters:
                            a (obj): self
                            b (str): method name to be called
                            c (*): Data (if any) to be passed to the method.
                                    Note: It must be structured according to the given methods requirements.

                    Returns:
                            Return data is that which the calling method gives.
        '''
        method_name = str(_method_name)
        method      = getattr(self, method_name, lambda data: f"No valid key passed...\nkey={method_name}\nargs={data}")
        return method(*data) if data else method()

    def has_method(self, obj: type, method: type) -> type:
        ''' Checks if a given method exists. '''
        return callable(getattr(obj, method, None))

    def clear_children(self, widget: type) -> None:
        ''' Clear children of a gtk widget. '''
        for child in widget.get_children():
            widget.remove(child)
