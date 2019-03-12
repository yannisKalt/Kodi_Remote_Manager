# -*- coding: utf-8 -*-

'''
    Tulip routine libraries, based on lambda's lamlib
    Author Twilight0

        License summary below, for more details please read license.txt file

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 2 of the License, or
        (at your option) any later version.
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from __future__ import absolute_import

import hashlib, json
from ast import literal_eval as evaluate
from tulip import control
from tulip.compat import database, str, iteritems


def add(url, table=control.bookmarksFile):

    try:

        data = json.loads(url)

        dbid = hashlib.md5()

        for i in data['bookmark']:
            dbid.update(str(i))
        for i in data['action']:
            dbid.update(str(i))

        dbid = str(dbid.hexdigest())

        item = dict((k,v) for k, v in iteritems(data) if not k == 'bookmark')
        item = repr(item)

        control.makeFile(control.dataPath)
        dbcon = database.connect(table)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS bookmark (""dbid TEXT, ""item TEXT, ""UNIQUE(dbid)"");")
        dbcur.execute("DELETE FROM bookmark WHERE dbid = '{}'".format(dbid))
        dbcur.execute("INSERT INTO bookmark Values (?, ?)", (dbid, item))
        dbcon.commit()

    except Exception:

        pass


def delete(url, table=control.bookmarksFile):

    try:

        data = json.loads(url)

        dbid = hashlib.md5()

        for i in data['delbookmark']:
            dbid.update(str(i))

        for i in data['action']:
            dbid.update(str(i))

        dbid = str(dbid.hexdigest())

        control.makeFile(control.dataPath)
        dbcon = database.connect(table)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS bookmark (""dbid TEXT, ""item TEXT, ""UNIQUE(dbid)"");")
        dbcur.execute("DELETE FROM bookmark WHERE dbid = '{}'".format(dbid))
        dbcon.commit()

        control.refresh()

    except Exception:

        pass


def get(table=control.bookmarksFile):

    try:

        control.makeFile(control.dataPath)
        dbcon = database.connect(table)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT * FROM bookmark")
        items = dbcur.fetchall()
        try:
            items = [evaluate(i[1].encode('utf-8')) for i in items]
        except Exception:
            items = [evaluate(i[1]) for i in items]

        return items

    except Exception:

        pass


