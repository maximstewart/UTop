# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class BuilderWrapper(Gtk.Builder):
    """docstring for BuilderWrapper."""

    def __init__(self):
        super(BuilderWrapper, self).__init__()

        self.objects = {}

    def get_object(self, id: str, use_gtk: bool = True) -> any:
        if not use_gtk:
            return self.objects[id]

        return super(BuilderWrapper, self).get_object(id)

    def expose_object(self, id: str, object: any, use_gtk: bool = True) -> None:
        if not use_gtk:
            self.objects[id] = object
        else:
            super(BuilderWrapper, self).expose_object(id, object)

    def dereference_object(self, id: str) -> None:
        del self.objects[id]
