# Python imports
import os

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Vte

# Application imports
from libs.dto.event import Event



class VteWidgetException(Exception):
    ...



class VteWidget(Vte.Terminal):
    """
        https://stackoverflow.com/questions/60454326/how-to-implement-a-linux-terminal-in-a-pygtk-app-like-vscode-and-pycharm-has
    """

    def __init__(self):
        super(VteWidget, self).__init__()

        self.cd_cmd_prefix = ("cd".encode(), "cd ".encode())
        self.dont_process  = False

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()
        self._do_session_spawn()

        self.show()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("vte-widget")

        self.set_clear_background(False)
        self.set_enable_sixel(True)
        self.set_cursor_shape( Vte.CursorShape.IBEAM )

    def _setup_signals(self):
        self.connect("commit", self._commit)

    def _subscribe_to_events(self):
        event_system.subscribe("update_term_path", self.update_term_path)

    def _load_widgets(self):
        ...

    def _do_session_spawn(self):
        self.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            settings_manager.get_home_path(),
            ["/bin/bash"],
            [],
            GLib.SpawnFlags.DEFAULT,
            None, None,
        )

        # Note:  '-->:' is used as a delimiter to split on to get command actual.
        #              !!!  DO NOT REMOVE UNLESS CODE UPDATED ACCORDINGLY  !!!
        startup_cmds = [
            "env -i /bin/bash --noprofile --norc\n",
            "export TERM='xterm-256color'\n",
            "export LC_ALL=C\n",
            "export XDG_RUNTIME_DIR='/run/user/1000'\n",
            "export DISPLAY=:0\n",
            f"export XAUTHORITY='{settings_manager.get_home_path()}/.Xauthority'\n",
            f"\nexport HOME='{settings_manager.get_home_path()}'\n",
            "export PS1='\\h@\\u \\W -->: '\n",
            "clear\n"
        ]

        for i in startup_cmds:
            self.run_command(i)

    def _commit(self, terminal, text, size):
        if self.dont_process:
            self.dont_process = False
            return

        if not text.encode() == "\r".encode(): return

        text, attributes = self.get_text()
        lines            = text.strip().splitlines()
        command_ran      = None

        try:
            command_ran  = lines[-1].split("-->:")[1].strip()
        except VteWidgetException as e:
            logger.debug(e)
            return

        if not command_ran[0:3].encode() in self.cd_cmd_prefix:
            return

        target_path = command_ran.split( command_ran[0:3] )[1]
        if target_path in (".", "./"): return

        if not target_path:
            target_path = settings_manager.get_home_path()

        event = Event("pty_path_updated", "", target_path)
        event_system.emit("handle_bridge_event", (event,))

    def update_term_path(self, fpath: str):
        self.dont_process = True

        cmds = [f"cd '{fpath}'\n", "clear\n"]
        for cmd in cmds:
            self.run_command(cmd)

    def run_command(self, cmd: str):
        self.feed_child_binary(bytes(cmd, 'utf8'))