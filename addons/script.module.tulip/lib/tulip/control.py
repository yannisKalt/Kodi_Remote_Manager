# -*- coding: utf-8 -*-

'''
    Tulip library
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''


from __future__ import absolute_import, division

from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
import os, json, time
from tulip.init import syshandle
from tulip.compat import basestring, is_py3


integer = 1000
addon = xbmcaddon.Addon
lang = addon().getLocalizedString
setting = addon().getSetting
setSetting = addon().setSetting
addonInfo = addon().getAddonInfo

addItem = xbmcplugin.addDirectoryItem
addItems = xbmcplugin.addDirectoryItems
directory = xbmcplugin.endOfDirectory
content = xbmcplugin.setContent
setproperty = xbmcplugin.setProperty
setcategory = xbmcplugin.setPluginCategory
resolve = xbmcplugin.setResolvedUrl
sortmethod = xbmcplugin.addSortMethod

infoLabel = xbmc.getInfoLabel
condVisibility = xbmc.getCondVisibility
jsonrpc = xbmc.executeJSONRPC  # keeping this for compatibility
keyboard = xbmc.Keyboard
sleep = xbmc.sleep
execute = xbmc.executebuiltin
skin = xbmc.getSkinDir()
player = xbmc.Player
monitor = xbmc.Monitor
wait = monitor().waitForAbort
aborted = monitor().abortRequested
cleanmovietitle = xbmc.getCleanMovieTitle
getregion = xbmc.getRegion

window = xbmcgui.Window(10000)
dialog = xbmcgui.Dialog()
progressDialog = xbmcgui.DialogProgress()
progressDialogGB = xbmcgui.DialogProgressBG()
windowDialog = xbmcgui.WindowDialog()
button = xbmcgui.ControlButton
image = xbmcgui.ControlImage
alphanum_input = xbmcgui.INPUT_ALPHANUM
password_input = xbmcgui.INPUT_PASSWORD
hide_input = xbmcgui.ALPHANUM_HIDE_INPUT
input_date = xbmcgui.INPUT_DATE
input_time = xbmcgui.INPUT_TIME
verify = xbmcgui.PASSWORD_VERIFY
item = xbmcgui.ListItem

openFile = xbmcvfs.File
makeFile = xbmcvfs.mkdir
makeFiles = xbmcvfs.mkdirs
deleteFile = xbmcvfs.delete
deleteDir = xbmcvfs.rmdir
listDir = xbmcvfs.listdir
exists = xbmcvfs.exists
copy = xbmcvfs.copy
rename = xbmcvfs.rename
join = os.path.join


def kodi_version():

    """
    Get kodi version as a float. Useful for various conditionals,
    especially when doing operations that old versions do not support
    :return: float
    """

    return float(addon('xbmc.addon').getAddonInfo('version')[:4])


if is_py3:
    legalfilename = xbmcvfs.makeLegalFilename
    transPath = xbmcvfs.translatePath
else:
    legalfilename = xbmc.makeLegalFilename
    transPath = xbmc.translatePath

skinPath = transPath('special://skin/')
addonPath = transPath(addonInfo('path'))
dataPath = transPath(addonInfo('profile'))
settingsFile = join(dataPath, 'settings.xml')
bookmarksFile = join(dataPath, 'bookmarks.db')
cacheFile = join(dataPath, 'cache.db')


def name():

    return addonInfo('name')


def version():

    return addonInfo('version')


def fanart():

    return addonInfo('fanart')


def icon():

    return addonInfo('icon')


def infoDialog(message, heading=addonInfo('name'), icon='', time=3000, sound=False):

    if icon == '':
        icon = addonInfo('icon')

    try:

        dialog.notification(heading, message, icon, time, sound=sound)

    except Exception:

        execute("Notification({0}, {1}, {2}, {3})".format(heading, message, time, icon))


def okDialog(heading, line1):

    return dialog.ok(heading, line1)


def yesnoDialog(line1, heading=addonInfo('name'), nolabel='', yeslabel=''):

    if is_py3:
        return dialog.yesno(heading, message=line1, nolabel=nolabel, yeslabel=yeslabel)
    else:
        return dialog.yesno(heading, line1=line1, nolabel=nolabel, yeslabel=yeslabel)


def selectDialog(list, heading=addonInfo('name'), autoclose=0, preselect=-1, useDetails=False):

    if kodi_version() >= 17.0:
        return dialog.select(heading, list, autoclose=autoclose, preselect=preselect, useDetails=useDetails)
    else:
        return dialog.select(heading, list)


def inputDialog(heading=name(), default='', type=alphanum_input, option=0, autoclose=0):

    try:
        return dialog.input(heading=heading, default=default, type=type, option=option, autoclose=autoclose)
    except Exception:
        return dialog.input(heading=heading, defaultt=default, type=type, option=option, autoclose=autoclose)


if kodi_version() >= 18.0:

    def text_viewer(heading, text, use_mono=False):

        dialog.textviewer(heading, text, use_mono)

else:

    def text_viewer(heading, text):

        dialog.textviewer(heading, text)


class WorkingDialog(object):

    def __init__(self):

        busy()

    def __enter__(self):

        return self

    def __exit__(self):

        idle()


class ProgressDialog(object):

    pd = None

    def __init__(self, heading, line1='', background=False, active=True, timer=0):

        self.begin = time.time()
        self.timer = timer
        self.background = background
        self.heading = heading

        if active and not timer:

            self.pd = self.__create_dialog(line1)
            self.pd.update(0)

    def __create_dialog(self, line1):

        if self.background:

            pd = xbmcgui.DialogProgressBG()
            pd.create(self.heading, line1)

        else:

            pd = xbmcgui.DialogProgress()
            pd.create(self.heading, line1)

        return pd

    def __enter__(self):

        return self

    def __exit__(self, type, value, traceback):

        if self.pd is not None:

            self.pd.close()

    def is_canceled(self):

        if self.pd is not None and not self.background:

            return self.pd.iscanceled()

        else:

            return False

    def update(self, percent, line1=''):

        if self.pd is None and self.timer and (time.time() - self.begin) >= self.timer:

            self.pd = self.__create_dialog(line1)

        if self.pd is not None:

            if self.background:

                self.pd.update(percent, self.heading, line1)

            else:

                self.pd.update(percent, line1)


class CountdownDialog(object):

    INTERVALS = 5

    pd = None

    def __init__(self, heading, line1='', expiration='', active=True, countdown=60, interval=5):

        self.heading = heading
        self.countdown = countdown
        self.interval = interval
        self.expiration = expiration
        self.line1 = line1

        if active:

            pd = xbmcgui.DialogProgress()

            if not self.expiration:

                expiration = 'Expires in: {} seconds'.format(countdown)

            else:

                if isinstance(expiration, int):
                    expiration = lang(expiration).format(countdown)
                else:
                    expiration = expiration.format(countdown)

            pd.create(self.heading, self.line1 + '[CR]' + expiration)
            pd.update(100)

            self.pd = pd

    def __enter__(self):

        return self

    def __exit__(self, type, value, traceback):

        if self.pd is not None:
            self.pd.close()

    def start(self, func, args=None, kwargs=None):

        if args is None: args = []
        if kwargs is None: kwargs = {}

        result = func(*args, **kwargs)

        if result:
            return result

        start = time.time()
        expires = time_left = int(self.countdown)
        interval = self.interval

        while time_left > 0:

            for _ in list(range(CountdownDialog.INTERVALS)):

                sleep(int(round(interval * 1000 / CountdownDialog.INTERVALS)))

                if self.is_canceled():
                    return

                time_left = expires - int(time.time() - start)

                if time_left < 0:
                    time_left = 0

                progress = int(round(time_left * 100 / expires))
                pg_text = 'Expires in: %s seconds' % time_left if not self.expiration else ''

                self.update(progress, line1=self.line1 + '[CR]' + pg_text)

            result = func(*args, **kwargs)
            if result:
                return result

    def is_canceled(self):
        if self.pd is None:
            return False
        else:
            return self.pd.iscanceled()

    def update(self, percent, line1=''):
        if self.pd is not None:
            self.pd.update(percent, line1)


def read(file_, numBytes=0):

    return openFile(file_).read(numBytes)


def readbytes(file_, numBytes=0):

    return openFile(file_).readBytes(numBytes)


def openSettings(query=None, id=addonInfo('id'), execute_=True):

    idle()

    if execute_:
        execute('Addon.OpenSettings({0})'.format(id))
    else:
        addon(id).openSettings()

    if query is not None:

        try:

            c, f = query.split('.')
            if kodi_version() >= 18.0:
                execute('SetFocus(-{0})'.format(100 - int(c)))
                if int(f):
                    execute('SetFocus(-{0})'.format(80 - int(f)))
            else:
                execute('SetFocus({0})'.format(100 + int(c)))
                if int(f):
                    execute('SetFocus({0})'.format(200 + int(f)))

        except Exception:

            pass


def playlist(mode=1):

    """
    # mode=1 for video and mode=0 for music/audio
    """

    return xbmc.PlayList(mode)


def openPlaylist(playlist_type=None):

    if not playlist_type or playlist_type == 1:
        playlist_type = 'videoplaylist'
    elif playlist_type == 0:
        playlist_type = 'musicplaylist'

    return execute('ActivateWindow({0})'.format(playlist_type))


def move(source, destination):

    copy(source, destination)
    deleteFile(source)


def refresh():

    return execute('Container.Refresh')


def idle():

    if kodi_version() >= 18.0:
        execute('Dialog.Close(busydialognocancel)')
    else:
        execute('Dialog.Close(busydialog)')


def busy():

    if kodi_version() >= 18.0:
        execute('ActivateWindow(busydialognocancel)')
    else:
        execute('ActivateWindow(busydialog)')


def close_all():

    execute('Dialog.Close(all)')


def set_view_mode(view_mode):

    if isinstance(view_mode, int):
        view_mode = str(view_mode)

    return execute('Container.SetViewMode({0})'.format(view_mode))


# for compartmentalized theme addons
def addonmedia(icon, addonid=addonInfo('id'), theme=None, media_subfolder=True):

    if not theme:
        return join(addon(addonid).getAddonInfo('path'), 'resources', 'media' if media_subfolder else '', icon)
    else:
        return join(addon(addonid).getAddonInfo('path'), 'resources', 'media' if media_subfolder else '', theme, icon)


def sortmethods(method='unsorted', mask='%D'):

    """
    Function to sort directory items

    :param method: acceptable values are: TODO
    :param mask: acceptable values are: TODO
    :type method: str
    :type mask: str
    :return: call existing function and pass parameters
    :rtype: xbmcplugin.addSortMethod(handle=syshandle, sortMethod=int)
    :note: Method to sort directory items
    """

    #  "%A" "%B" "%C" "%D" ...

    if method == 'none':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_NONE, label2Mask=mask)
    elif method == 'label':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL, label2Mask=mask)
    elif method == 'label_ignore_the':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE, label2Mask=mask)
    elif method == 'date':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    elif method == 'size':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_SIZE)
    elif method == 'file':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_FILE, label2Mask=mask)
    elif method == 'drive_type':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_DRIVE_TYPE)
    elif method == 'tracknum':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_TRACKNUM, label2Mask=mask)
    elif method == 'duration':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_DURATION)
    elif method == 'title':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_TITLE, label2Mask=mask)
    elif method == 'title_ignore_the':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE, label2Mask=mask)
    elif method == 'artist':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_ARTIST)
    elif method == 'artist_ignore_the':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_ARTIST_IGNORE_THE)
    elif method == 'album':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_ALBUM)
    elif method == 'album_ignore_the':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_ALBUM_IGNORE_THE)
    elif method == 'genre':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_GENRE)
    elif method == 'year':
        try:
            return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_YEAR)
        except Exception:
            return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    elif method == 'video_rating':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING)
    elif method == 'program_count':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT)
    elif method == 'playlist_order':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_PLAYLIST_ORDER)
    elif method == 'episode':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_EPISODE)
    elif method == 'video_title':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_TITLE, label2Mask=mask)
    elif method == 'video_sort_title':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE, label2Mask=mask)
    elif method == 'video_sort_title_ignore_the':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE, label2Mask=mask)
    elif method == 'production_code':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_PRODUCTIONCODE)
    elif method == 'song_rating':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_SONG_RATING)
    elif method == 'mpaa_rating':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING)
    elif method == 'video_runtime':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
    elif method == 'studio':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_STUDIO)
    elif method == 'studio_ignore_the':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_STUDIO_IGNORE_THE)
    elif method == 'unsorted':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED, label2Mask=mask)
    elif method == 'bitrate':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_BITRATE)
    elif method == 'listeners':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_LISTENERS)
    elif method == 'country':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_COUNTRY)
    elif method == 'date_added':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_DATEADDED)
    elif method == 'full_path':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_FULLPATH, label2Mask=mask)
    elif method == 'label_ignore_folders':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_FOLDERS, label2Mask=mask)
    elif method == 'last_played':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_LASTPLAYED)
    elif method == 'play_count':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_PLAYCOUNT)
    elif method == 'channel':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_CHANNEL, label2Mask=mask)
    elif method == 'date_taken':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_DATE_TAKEN)
    elif method == 'video_user_rating':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_USER_RATING)
    elif method == 'song_user_rating':
        return sortmethod(handle=syshandle, sortMethod=xbmcplugin.SORT_METHOD_SONG_USER_RATING)
    else:
        pass


def json_rpc(command):

    # This function was taken from tknorris's kodi.py

    if not isinstance(command, basestring):
        command = json.dumps(command)
    response = jsonrpc(command)

    return json.loads(response)


def addon_details(addon_id, fields=None):

    """
    :param addon_id: Any addon id as string
    :param fields: Possible fields as list [
      "name",
      "version",
      "summary",
      "description",
      "path",
      "author",
      "thumbnail",
      "disclaimer",
      "fanart",
      "dependencies",
      "broken",
      "extrainfo",
      "rating",
      "enabled",
      "installed"
    ]
    Default argument: ["enabled"]
    :return: Dictionary
    """

    if fields is None:
        fields = ["enabled"]

    command = {
        "jsonrpc": "2.0", "method": "Addons.GetAddonDetails", "id": 1, "params": {
            "addonid": addon_id, "properties": fields
        }
    }

    result = json_rpc(command)['result']['addon']

    return result


def enable_addon(addon_id, enable=True):

    """Enable/Disable an addon via json-rpc"""

    command = {
        "jsonrpc":"2.0", "method": "Addons.SetAddonEnabled", "params": {"addonid": addon_id, "enabled": enable}, "id": 1
    }

    json_rpc(command)


def set_gui_setting(_setting_, value):

    """Change a gui setting via json-rpc"""

    json_cmd = {
        "jsonrpc": "2.0", "method": "Settings.SetSettingValue", "params": {"setting": _setting_, "value": value}, "id": 1
    }

    json_rpc(json_cmd)


def get_a_setting(_setting_):

    """Return the state of a gui setting as dictionary"""

    json_cmd = {
        "jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": _setting_}, "id": 1
    }

    return json_rpc(json_cmd)


def get_skin_bool_setting(setting_id):

    return bool(condVisibility('Skin.HasSetting({0})'.format(setting_id)))


def set_skin_bool_setting(setting_id, state='true'):

    return execute('Skin.SetBool({0},{1})'.format(setting_id, state))


def set_skin_string_setting(setting_id, string):

    return execute('Skin.SetString({0},{1})'.format(setting_id, string))


def set_default_addon(extensionpoint):

    """
    This function is able to set a default addon for an extension point for example "xbmc.gui.skin"
    :param extensionpoint: An extension point in the form of string
    :return: None
    """

    execute('Addon.Default.Set({0})'.format(extensionpoint))


def activate_screensaver():

    execute('ActivateScreensaver')


def get_info_label(infolabel):

    return infoLabel("{0}".format(infolabel))


def conditional_visibility(boolean_condition):

    """
    List of Kodi boolean conditions here: https://kodi.wiki/view/List_of_boolean_conditions
    :param boolean_condition: str
    :return: bool
    """

    return bool(condVisibility('{0}'.format(boolean_condition)))


def active_mode():

    def visible_window(window_id):

        boolean = bool(condVisibility('Window.IsVisible({0})'.format(window_id)))

        return boolean

    if visible_window('videos'):
        window_ = 'videos'
    elif visible_window('music'):
        window_ = 'music'
    elif visible_window('pictures'):
        window_ = 'pictures'
    elif visible_window('programs'):
        window_ = 'programs'
    else:
        window_ = 'other'

    return window_


def quit_kodi():

    busy()

    execute('Quit')


def reload_skin():

    execute('ReloadSkin()')


def android_activity(url, package=''):

    if package:
        package = ''.join(['"', package, '"'])

    return execute('StartAndroidActivity({0},"android.intent.action.VIEW","","{1}")'.format(package, url))


def open_web_browser(url):

    if condVisibility('system.platform.android'):

        return android_activity(url)

    else:

        import webbrowser

        return webbrowser.open(url)


def update_repositories():

    xbmc.executebuiltin('UpdateAddonRepos')


def update_addons():

    xbmc.executebuiltin('UpdateLocalAddons')


def install_addon(addon_id, send_yes=True):

    xbmc.executebuiltin('InstallAddon({0})'.format(addon_id))

    if send_yes:

        while not wait(1):
            if xbmc.getCondVisibility('Window.IsActive(yesnodialog)'):
                xbmc.executebuiltin('SendClick(yesnodialog,11)')
                break
            elif not xbmc.getCondVisibility('Window.IsActive(yesnodialog)'):
                break
