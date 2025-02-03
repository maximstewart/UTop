# Python imports
import os, subprocess

# Gtk imports
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import GdkPixbuf

# Application imports
from .controller_data import ControllerData
from .core_widget import CoreWidget



class Controller(ControllerData):
    def __init__(self, args, unknownargs):
        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()

        self.setup_controller_data()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        ...



    # NOTE: To be filled out after app data is actually working...
    def search_for_entry(self, widget, data = None):
        ...

    def set_list_group(self, widget):
        group       = widget.get_label().strip()
        group_items = self.core_widget.get_group(group)
        grid        = self.builder.get_object("program_list_bttns")

        children = grid.get_children()
        for child in children:
            child.disconnect(child.sig_id)
            grid.remove(child)

        row   = 0
        col   = 0
        icon_theme = Gtk.IconTheme.get_default()

        for item in group_items:
            button = self.generate_app_button(icon_theme, item)
            grid.attach(button, col, row, 1, 1)

            col += 1
            if col == 4:
                col = 0
                row += 1



    def generate_app_button(self, icon_theme, item):
        title    = item["title"]
        exec_str = item[
            "exec" if not item["exec"] in ("", None) else "tryExec"
        ]

        button = Gtk.Button(label = title)
        button.sig_id = button.connect("clicked", self.test_exec, exec_str)

        if self.show_image:
            _icon = item["icon"]

            if os.path.exists(_icon):
                icon = self.get_icon_from_path(_icon)
            else:
                icon = self.get_icon_from_gio(icon_theme, _icon)

            button.set_image(icon)
            button.set_always_show_image(True)

        button.show_all()
        return button

    def get_icon_from_path(self, path):
        pixbuf = GdkPixbuf.PixbufAnimation.new_from_file(path) \
                                            .get_static_image() \
                                            .scale_simple(32, 32, \
                                            GdkPixbuf.InterpType.BILINEAR)

        return Gtk.Image.new_from_pixbuf(pixbuf)


    def get_icon_from_gio(self, icon_theme, icon_name):
        gio_icon = Gio.Icon.new_for_string(icon_name)
        pixbuf   = None

        # Note:  https://docs.gtk.org/gtk3/enum.IconSize.html
        for i in [6, 5, 3, 4, 2, 1]:
            icon_info = Gtk.IconTheme.lookup_by_gicon(icon_theme, gio_icon, i, Gtk.IconLookupFlags.FORCE_REGULAR)
            if not icon_info: continue

            pixbuf = icon_info.load_icon().scale_simple(32, 32, 2) # 2 = BILINEAR and is best by default
            break

        return Gtk.Image.new_from_pixbuf( pixbuf )


    def test_exec(self, widget, _command):
        command = _command.split("%")[0]
        DEVNULL = open(os.devnull, 'w')
        subprocess.Popen(command.split(), start_new_session=True, stdout=DEVNULL, stderr=DEVNULL)



    def _subscribe_to_events(self):
        event_system.subscribe("handle_file_from_ipc", self.handle_file_from_ipc)

    def handle_file_from_ipc(self, path: str) -> None:
        print(f"Path From IPC: {path}")

    def load_glade_file(self):
        self.builder     = Gtk.Builder()
        self.builder.add_from_file(settings.get_glade_file())
        settings.set_builder(self.builder)
        self.core_widget = CoreWidget()

        settings.register_signals_to_builder([self, self.core_widget])

    def get_core_widget(self):
        self.setup_toggle_event()
        return self.core_widget

    def on_hide_window(self, data = None):
        """Handle a request to hide/show the window"""
        if not self.window.get_property('visible'):
            self.window.show()
            self.window.grab_focus()
            # NOTE:  Need here to enforce sticky after hide and reshow.
            self.window.stick()
        else:
            self.hidefunc()

    def on_global_key_release_controller(self, widget: type, event: type) -> None:
        """Handler for keyboard events"""
        keyname = Gdk.keyval_name(event.keyval).lower()
        if keyname.replace("_l", "").replace("_r", "") in ["control", "alt", "shift"]:
            if "control" in keyname:
                self.ctrl_down    = False
            if "shift" in keyname:
                self.shift_down   = False
            if "alt" in keyname:
                self.alt_down     = False


        mapping = keybindings.lookup(event)
        if mapping:
            getattr(self, mapping)()
            return True
        else:
            print(f"on_global_key_release_controller > key > {keyname}")
            print(f"Add logic or remove this from: {self.__class__}")


    def get_clipboard_data(self) -> str:
        proc    = subprocess.Popen(['xclip','-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
        retcode = proc.wait()
        data    = proc.stdout.read()
        return data.decode("utf-8").strip()

    def set_clipboard_data(self, data: type) -> None:
        proc = subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE)
        proc.stdin.write(data)
        proc.stdin.close()
        retcode = proc.wait()