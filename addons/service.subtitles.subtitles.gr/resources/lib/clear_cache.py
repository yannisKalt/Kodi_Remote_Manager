# -*- coding: utf-8 -*-

'''
    Subtitles.gr Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from xbmc import translatePath
from xbmcgui import Dialog

try:
    from sqlite3 import dbapi2 as database
except ImportError:
    from pysqlite2 import dbapi2 as database


def action():

    table = ['rel_list', 'rel_lib']

    filename = translatePath('special://profile/addon_data/service.subtitles.subtitles.gr/cache.db')

    dbcon = database.connect(filename)
    dbcur = dbcon.cursor()

    for t in table:

        try:

            dbcur.execute("DROP TABLE IF EXISTS {0}".format(t))
            dbcur.execute("VACUUM")
            dbcon.commit()

        except BaseException:

            pass


if __name__ == '__main__':

    action()

    Dialog().notification('Subtitles.gr', 'OK', time=2, sound=False)
