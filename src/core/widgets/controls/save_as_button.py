# Python imports
import os

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio

# Application imports



class SaveAsButton(Gtk.Button):
    def __init__(self):
        super(SaveAsButton, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_label("Save As")
        self.set_image( Gtk.Image.new_from_icon_name("gtk-save-as", 4) )
        self.set_always_show_image(True)
        self.set_image_position(1) # Left - 0, Right = 1
        self.set_hexpand(False)

    def _setup_signals(self):
        self.connect("released", self._save_as)

    def _subscribe_to_events(self):
        event_system.subscribe("save-as", self._save_as)

    def _load_widgets(self):
        ...

    def _save_as(self, widget = None, eve = None, gfile = None):
        start_dir = None
        _gfile    = None

        chooser = Gtk.FileChooserDialog("Save File As...", None,
                                        Gtk.FileChooserAction.SAVE,
                                        (
                                            Gtk.STOCK_CANCEL,
                                            Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_SAVE_AS,
                                            Gtk.ResponseType.OK
                                        )
        )

        # chooser.set_select_multiple(False)

        response = chooser.run()
        if not response == Gtk.ResponseType.OK:
            chooser.destroy()
            return _gfile

        file = chooser.get_filename()
        if not file:
            chooser.destroy()
            return _gfile

        path   = file if os.path.isabs(file) else os.path.abspath(file)
        _gfile = Gio.File.new_for_path(path) 

        chooser.destroy()

        logger.debug(f"File To Save As:  {_gfile}")
        return _gfile
