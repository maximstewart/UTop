# Python imports

# Lib imports
import gi
from gi.repository import GLib

# Application imports




class IPCSignalsMixin:
    """ IPCSignalsMixin handle messages from another starting {APP_NAME} process. """

    def print_to_console(self, message = None):
        logger.debug(message)

    def handle_file_from_ipc(self, fpath: str) -> None:
        logger.debug(f"File From IPC: {fpath}")
        GLib.idle_add(
            self.broadcast_message, "handle-file", (fpath,)
        )

    def handle_dir_from_ipc(self, fpath: str) -> None:
        logger.debug(f"Dir From IPC: {fpath}")
        GLib.idle_add(
            self.broadcast_message, "handle-folder", (fpath,)
        )

    def broadcast_message(self, message_type: str = "none", data: () = ()) -> None:
        event_system.emit(message_type, data)