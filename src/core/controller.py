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
    def search_for_entry(self, widget, data=None):
        ...

    def set_list_group(self, widget):
        group       = widget.get_label().strip()
        group_items = self.core_widget.get_group(group)
        grid        = self.builder.get_object("programListBttns")

        children = grid.get_children()
        for child in children:
            grid.remove(child)

        row = 0
        col = 0
        for item in group_items:
            title   = item["title"]
            if not item["exec"] in ("", None):
                exec = item["exec"]
            else:
                exec = item["tryExec"]

            button = Gtk.Button(label=title)
            button.connect("clicked", self.test_exec, exec)
            if self.show_image:
                if os.path.exists(item["icon"]):
                    pixbuf = GdkPixbuf.PixbufAnimation.new_from_file(item["icon"]) \
                                                        .get_static_image() \
                                                        .scale_simple(64, 64, \
                                                        GdkPixbuf.InterpType.BILINEAR)

                    icon = Gtk.Image.new_from_pixbuf(pixbuf)
                else:
                    gio_icon = Gio.Icon.new_for_string(item["icon"])
                    icon = Gtk.Image.new_from_gicon(gio_icon, 64)

                button.set_image(icon)
                button.set_always_show_image(True)

            button.show_all()
            grid.attach(button, col, row, 1, 1)

            col += 1
            if col == 4:
                col = 0
                row += 1

            # grid.add(button)

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

    def on_hide_window(self, data=None):
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
