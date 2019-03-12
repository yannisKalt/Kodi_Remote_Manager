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

__all__ = ['log_notice', 'log_debug', 'log_info', 'log_warning', 'log_error']

from kodi_six import xbmc
from tulip import control

LOGDEBUG = xbmc.LOGDEBUG
LOGERROR = xbmc.LOGERROR
LOGFATAL = xbmc.LOGFATAL
LOGINFO = xbmc.LOGINFO
LOGNONE = xbmc.LOGNONE
LOGNOTICE = xbmc.LOGNOTICE
LOGSEVERE = xbmc.LOGSEVERE
LOGWARNING = xbmc.LOGWARNING


def log_debug(msg):
    log(msg, level=LOGDEBUG)


def log_notice(msg):
    log(msg, level=LOGNOTICE)


def log_warning(msg):
    log(msg, level=LOGWARNING)


def log_error(msg):
    log(msg, level=LOGERROR)


def log_info(msg):
    log(msg, level=LOGINFO)


def log_severe(msg):
    log(msg, level=LOGSEVERE)


def log(msg, level=LOGDEBUG, setting='debug'):
    # override message level to force logging when addon logging turned on
    if control.setting(setting) == 'true' and level == LOGDEBUG:
        level = LOGNOTICE

    try:
        xbmc.log('{0}, {1}:: {2}'.format(control.addonInfo('name'), control.addonInfo('version'), msg), level)
    except Exception:
        try:
            xbmc.log('{0}'.format(msg), level)
        except Exception as reason:
            xbmc.log('Logging Failure: {0}' % reason, level)
