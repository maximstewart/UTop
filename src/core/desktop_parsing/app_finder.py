# Python imports
import os
import logging
from collections import OrderedDict
from itertools import chain
from typing import Generator, List

# Lib imports
from gi.repository import Gio
from xdg.BaseDirectory import xdg_config_home, xdg_cache_home, xdg_data_dirs, xdg_data_home


# Application imports
from .file_finder import find_files
from .db.KeyValueDb import KeyValueDb




DEFAULT_BLACKLISTED_DIRS = [
    '/usr/share/locale',
    '/usr/share/app-install',
    '/usr/share/kservices5',
    '/usr/share/fk5',
    '/usr/share/kservicetypes5',
    '/usr/share/applications/screensavers',
    '/usr/share/kde4',
    '/usr/share/mimelnk'
]

# Use utop_cache dir because of the WebKit bug
# https://bugs.webkit.org/show_bug.cgi?id=151646
CACHE_DIR = os.path.join(xdg_cache_home, 'utop_cache')

# Spec: https://specifications.freedesktop.org/menu-spec/latest/ar01s02.html
DESKTOP_DIRS = list(filter(os.path.exists, [os.path.join(dir, "applications") for dir in xdg_data_dirs]))

logger = logging.getLogger(__name__)




def find_desktop_files(dirs: List[str] = None, pattern: str = "*.desktop") -> Generator[str, None, None]:
    """
        Returns deduped list of .desktop files (full paths)

        :param list dirs:
        :rtype: list
    """

    if dirs is None:
        dirs = DESKTOP_DIRS

    all_files = chain.from_iterable(
                    map(lambda f: os.path.join(f_path, f), find_files(f_path, pattern)) for f_path in dirs
                )

    # NOTE: Dedup desktop file according to follow XDG data dir order.
    #       Specifically the first file name (i.e. firefox.desktop) take precedence
    #       and other files with the same name should be ignored
    deduped_file_dict = OrderedDict()
    for file_path in all_files:
        file_name = os.path.basename(file_path)
        if file_name not in deduped_file_dict:
            deduped_file_dict[file_name] = file_path

    deduped_files = deduped_file_dict.values()

    blacklisted_dirs = DEFAULT_BLACKLISTED_DIRS
    for file in deduped_files:
        try:
            if any([file.startswith(dir) for dir in blacklisted_dirs]):
                continue
        except UnicodeDecodeError:
            continue

        yield file


def filter_app(app):
    """
        :param Gio.DesktopAppInfo app:
        :returns: True if app can be added to the database
    """
    return app and not (app.get_is_hidden() or app.get_nodisplay()
                                            or app.get_string('Type') != 'Application'
                                            or not app.get_string('Name'))


def read_desktop_file(file):
    """
        :param str file: path to .desktop
        :rtype: :class:`Gio.DesktopAppInfo` or :code:`None`
    """
    try:
        return Gio.DesktopAppInfo.new_from_filename(file)
    except Exception as e:
        logger.info('Could not read "%s": %s', file, e)
        return None


def find_apps(dirs=None):
    """
        :param list dirs: list of paths to `*.desktop` files
        :returns: list of :class:`Gio.DesktopAppInfo` objects
    """
    if dirs is None:
        dirs = DESKTOP_DIRS

    return list(filter(filter_app, map(read_desktop_file, find_desktop_files(dirs))))


def find_apps_cached(dirs=None):
    """
        :param list dirs: list of paths to `*.desktop` files
        :returns: list of :class:`Gio.DesktopAppInfo` objects

        Pseudo code:
        >>> if cache hit:
        >>>     take list of paths from cache
        >>>     yield from filter(filter_app, map(read_desktop_file, cached_paths))
        >>> yield from find_apps()
        >>> save new paths to the cache
    """
    if dirs is None:
        dirs = DESKTOP_DIRS

    desktop_file_cache_dir = os.path.join(CACHE_DIR, 'desktop_dirs.db')
    cache = KeyValueDb(desktop_file_cache_dir).open()
    desktop_dirs = cache.find('desktop_dirs')

    if desktop_dirs:
        for dir in desktop_dirs:
            app_info = read_desktop_file(dir)
            if filter_app(app_info):
                yield app_info
        logger.info('Found %s apps in cache', len(desktop_dirs))

    new_desktop_dirs = []

    for app_info in find_apps(DESKTOP_DIRS):
        yield app_info
        new_desktop_dirs.append(app_info.get_filename())

    cache.put('desktop_dirs', new_desktop_dirs)
    cache.commit()
    logger.info('Found %s apps in the system', len(new_desktop_dirs))
