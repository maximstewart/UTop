# Python imports
import os
import subprocess

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GdkPixbuf

# Application imports



class CategoryWidget(Gtk.Grid):
    def __init__(self):
        super(CategoryWidget, self).__init__()

        self.ctx          = self.get_style_context()

        self.column_count = 4

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_row_spacing(10)
        self.set_column_spacing(10)
        self.set_row_homogeneous(True)
        self.set_column_homogeneous(True)

        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.ctx.add_class("category-widget")

    def _setup_signals(self):
        event_system.subscribe("load-active-category", self.load_active_category)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        event_system.emit("refresh-active-category")

    def load_active_category(self, app_list: [] = []):
        self.clear_children()

        row   = 0
        col   = 0
        icon_theme = Gtk.IconTheme.get_default()

        for app in app_list:
            button = self.generate_app_button(icon_theme, app)
            self.attach(button, col, row, 1, 1)

            col += 1
            if col == self.column_count:
                col = 0
                row += 1

    def generate_app_button(self, icon_theme, app: {} = {}):
        if not app: return

        title    = app["title"]
        exec_str = app[
            "exec" if not app["exec"] in ("", None) else "tryExec"
        ]

        button = Gtk.Button(label = title)
        button.sig_id = button.connect("clicked", self._do_exec, exec_str)

        icon_pth = app["icon"]
        icon = self.get_icon_from_path(icon_pth) \
                    if os.path.exists(icon_pth)  \
                    else                         \
                self.get_icon_from_gio(icon_theme, icon_pth)

        button.set_image(icon)
        button.set_always_show_image(True)

        button.show_all()
        return button

    def get_icon_from_path(self, path: str):
        pixbuf = GdkPixbuf.PixbufAnimation.new_from_file(path) \
                                            .get_static_image() \
                                            .scale_simple(32, 32, \
                                            GdkPixbuf.InterpType.BILINEAR)

        return Gtk.Image.new_from_pixbuf(pixbuf)

    def get_icon_from_gio(self, icon_theme, icon_name: str):
        gio_icon = Gio.Icon.new_for_string(icon_name)
        pixbuf   = None

        # Note:  https://docs.gtk.org/gtk3/enum.IconSize.html
        for i in [6, 5, 3, 4, 2, 1]:
            icon_info = Gtk.IconTheme.lookup_by_gicon(icon_theme, gio_icon, i, Gtk.IconLookupFlags.FORCE_REGULAR)
            if not icon_info: continue

            pixbuf = icon_info.load_icon().scale_simple(32, 32, 2) # 2 = BILINEAR and is best by default
            break

        return Gtk.Image.new_from_pixbuf( pixbuf )

    def _do_exec(self, widget, _command):
        command = _command.split("%")[0]
        subprocess.Popen(command.split(), start_new_session=True, stdout=None, stderr=None)

    def clear_children(self, app_list: [] = []):
        children = self.get_children()
        for child in children:
            child.disconnect(child.sig_id)
            self.remove(child)
            child.run_dispose()


