# Python imports
from datetime import datetime

# Gtk imports
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Wnck', '3.0')

from gi.repository import Gtk
from gi.repository import Wnck
from gi.repository import GObject
from gi.repository import GdkPixbuf
from xdg.DesktopEntry import DesktopEntry

# Application imports
from .desktop_parsing.app_finder import find_apps




class CoreWidget(Gtk.Box):
    def __init__(self):
        super(CoreWidget, self).__init__()
        self.builder     = settings.get_builder()
        self.time_label  = self.builder.get_object("time_lbl")

        self.orientation = 1  # 0 = horizontal, 1 = vertical

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()

        self.show_all()

        self.menu_objects = {
            "Accessories": [],
            "Multimedia": [],
            "Graphics": [],
            "Game": [],
            "Office": [],
            "Development": [],
            "Internet": [],
            "Settings": [],
            "System": [],
            "Wine": [],
            "Other": []
        }
        apps = find_apps()
        self.fill_menu_objects(apps)

        search_programs_entry = self.builder.get_object("search_programs_entry")
        search_programs_entry.hide()


    def fill_menu_objects(self, apps=[]):
        for app in apps:
            fPath    = app.get_filename()
            xdgObj   = DesktopEntry( fPath )

            title    = xdgObj.getName()
            groups   = xdgObj.getCategories()
            comment  = xdgObj.getComment()
            icon     = xdgObj.getIcon()
            mainExec = xdgObj.getExec()
            tryExec  = xdgObj.getTryExec()

            group    = ""
            if "Accessories" in groups or "Utility" in groups:
                group = "Accessories"
            elif "Multimedia" in groups or "Video" in groups or "Audio" in groups:
                group = "Multimedia"
            elif "Development" in groups:
                group = "Development"
            elif "Game" in groups:
                group = "Game"
            elif "Internet" in groups or "Network" in groups:
                group = "Internet"
            elif "Graphics" in groups:
                group = "Graphics"
            elif "Office" in groups:
                group = "Office"
            elif "System" in groups:
                group = "System"
            elif "Settings" in groups:
                group = "Settings"
            elif "Wine" in groups:
                group = "Wine"
            else:
                group = "Other"

            self.menu_objects[group].append(
                {
                    "title":  title,
                    "groups": groups,
                    "comment": comment,
                    "exec": mainExec,
                    "tryExec": tryExec,
                    "fileName": fPath.split("/")[-1],
                    "filePath": fPath,
                    "icon": icon
                }
            )

    def get_group(self, group):
        return self.menu_objects[group]



    def _setup_styling(self):
        self.set_orientation(1)
        self.set_vexpand(True)
        self.set_hexpand(True)

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        widget_grid_container = self.builder.get_object("widget_grid_container")

        time_lbl_eve_box = self.builder.get_object("time_lbl_eve_box")
        time_lbl_eve_box.connect("button_release_event", self._toggle_cal_popover)

        widget_grid_container.set_vexpand(True)
        widget_grid_container.set_hexpand(True)

        self.add( widget_grid_container )
        self.set_pager_widget()
        self.set_task_list_widget()

        # Must be after pager and task list inits
        self.display_clock()
        self._start_clock()


    def set_pager_widget(self):
        pager = Wnck.Pager.new()

        if self.orientation == 0:
            self.builder.get_object('taskbar_workspaces_hor').add(pager)
        else:
            self.builder.get_object('taskbar_workspaces_ver').add(pager)

        pager.set_hexpand(True)
        pager.show()

    def set_task_list_widget(self):
        tasklist = Wnck.Tasklist.new()
        tasklist.set_scroll_enabled(False)
        tasklist.set_button_relief(2)  # 0 = normal relief, 2 = no relief
        tasklist.set_grouping(1)       # 0 = mever group, 1 auto group, 2 = always group

        if self.orientation == 0:
            self.builder.get_object('taskbar_bttns_hor').add(tasklist)
        else:
            self.builder.get_object('taskbar_bttns_ver').add(tasklist)

        tasklist.set_vexpand(True)
        tasklist.set_include_all_workspaces(False)
        tasklist.set_orientation(self.orientation)
        tasklist.show()

    # Displays Timer
    def display_clock(self):
        now = datetime.now()
        hms = now.strftime("%I:%M %p")
        mdy = now.strftime("%m/%d/%Y")
        timeStr = hms + "\n" + mdy
        self.time_label.set_label(timeStr)
        return True

    def _start_clock(self):
        GObject.timeout_add(59000, self.display_clock)


    def _close_popup(self, widget, data = None):
        widget.hide()

    def _toggle_cal_popover(self, widget, eve):
        calendar_popup = self.builder.get_object('calendar_popup')
        if (calendar_popup.get_visible() == False):
            calendarWid = self.builder.get_object('calendarWid')
            now         = datetime.now()
            timeStr     = now.strftime("%m/%d/%Y")
            parts       = timeStr.split("/")
            month       = int(parts[0]) - 1
            day         = int(parts[1])
            year        = int(parts[2])
            calendarWid.select_day(day)
            calendarWid.select_month(month, year)
            calendar_popup.popup()
        else:
            calendar_popup.popdown()