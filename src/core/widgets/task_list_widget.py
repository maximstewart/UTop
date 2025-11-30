# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Wnck', '3.0')
from gi.repository import Gtk
from gi.repository import Wnck

# Application imports



class TaskListWidget(Gtk.ScrolledWindow):
    def __init__(self):
        super(TaskListWidget, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_hexpand(False)
        self.set_size_request(180, -1)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        viewport  = Gtk.Viewport()
        task_list = Wnck.Tasklist.new()
        vbox      = Gtk.Box()

        vbox.set_orientation(Gtk.Orientation.VERTICAL)


        task_list.set_scroll_enabled(False)
        task_list.set_button_relief(2)  # 0 = normal relief, 2 = no relief
        task_list.set_grouping(1)       # 0 = mever group, 1 auto group, 2 = always group

        task_list.set_vexpand(True)
        task_list.set_include_all_workspaces(False)
        task_list.set_orientation(1)    # 0 = horizontal, 1 = vertical

        vbox.add(task_list)
        viewport.add(vbox)
        self.add(viewport)
