# -*- coding: utf-8 -*-

'''
    Subtitles.gr
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

import sys
from random import choice
from os.path import split as os_split
from tulip import control
from tulip.compat import parse_qsl

syshandle = int(sys.argv[1])
sysaddon = sys.argv[0]
params = dict(parse_qsl(sys.argv[2].replace('?', '')))

action = params.get('action')
source = params.get('source')
url = params.get('url')
query = params.get('searchstring')
langs = params.get('languages')


def multichoice(filenames):

    if filenames is None or len(filenames) == 0:

        return

    elif len(filenames) >= 1:

        if len(filenames) == 1:
            return filenames[0]

        choices = [os_split(i)[1] for i in filenames]

        choices.insert(0, control.lang(32215))

        _choice = control.selectDialog(heading=control.lang(32214), list=choices)

        if _choice == 0:
            filename = choice(filenames)
        elif _choice != -1 and _choice <= len(filenames) + 1:
            filename = filenames[_choice - 1]
        else:
            filename = choice(filenames)

        return filename

    else:

        return
