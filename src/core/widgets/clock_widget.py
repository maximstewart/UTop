# Python imports
from datetime import datetime

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

# Application imports



class CalendarWidget(Gtk.Popover):
    def __init__(self):
        super(CalendarWidget, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        self.body = Gtk.Calendar()

        self.body.show()
        self.add(self.body)


class ClockWidget(Gtk.EventBox):
    def __init__(self):
        super(ClockWidget, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_size_request(180, -1)

        ctx = self.get_style_context()
        ctx.add_class("clock-widget")

    def _setup_signals(self):
        self.connect("button_release_event", self._toggle_cal_popover)


    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        self.calendar = CalendarWidget()
        self.label    = Gtk.Label()

        self.calendar.set_relative_to(self)

        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_margin_top(15)
        self.label.set_margin_bottom(15)
        self.label.set_margin_left(15)
        self.label.set_margin_right(15)

        self._update_face()
        self.add(self.label)

        GObject.timeout_add(59000, self._update_face)

    def _update_face(self):
        dt_now         = datetime.now()
        hours_mins_sec = dt_now.strftime("%I:%M %p")
        month_day_year = dt_now.strftime("%m/%d/%Y")
        time_str       = hours_mins_sec + "\n" + month_day_year

        self.label.set_label(time_str)

    def _toggle_cal_popover(self, widget, eve):
        if (self.calendar.get_visible() == True):
            self.calendar.popdown()
            return

        now         = datetime.now()
        timeStr     = now.strftime("%m/%d/%Y")
        parts       = timeStr.split("/")
        month       = int(parts[0]) - 1
        day         = int(parts[1])
        year        = int(parts[2])

        self.calendar.body.select_day(day)
        self.calendar.body.select_month(month, year)

        self.calendar.popup()





