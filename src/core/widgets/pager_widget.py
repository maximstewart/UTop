# Python imports

# Lib imports
import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck

# Application imports



class PagerWidget:
    def __init__(self):
        super(PagerWidget, self).__init__()

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
        ...

    def get_widget(self):
        return Wnck.Pager.new()
