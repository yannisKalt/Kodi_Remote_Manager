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

from tulip.compat import urlencode, quote_plus, iteritems, basestring, parse_qsl
from tulip import control
from kodi_six.xbmc import log


def add(
    items, cacheToDisc=True, content=None, mediatype=None, infotype='video', argv=None, as_playlist=False,
    pd_heading=None, pd_message='', clear_first=True, progress=False, category=None
):

    if argv is None:

        from tulip.init import sysaddon, syshandle

    else:

        sysaddon = argv[0]
        syshandle = int(argv[1])

    if items is None or len(items) == 0:
        return

    # sysicon = control.join(control.addonInfo('path'), 'resources', 'media')
    sysimage = control.addonInfo('icon')
    sysfanart = control.addonInfo('fanart')

    if progress:

        pd = control.progressDialogGB
        pd.create(heading=control.name() if not pd_heading else pd_heading, message=pd_message)

    else:

        pd = None

    if as_playlist and clear_first:

        control.playlist(1 if infotype == 'video' else 0).clear()

    for c, i in list(enumerate(items)):

        try:

            if progress:

                p = control.percent(c, len(items))
                pd.update(p)

            try:
                label = control.lang(i['title']).encode('utf-8')
            except Exception:
                label = i['title']

            if 'label' in i and not i['label'] == '0':
                label = i['label']

            if 'image' in i and not i['image'] == '0':
                image = i['image']
            elif 'poster' in i and not i['poster'] == '0':
                image = i['poster']
            elif 'icon' in i and not i['icon'] == '0':
                image = control.addonmedia(i['icon'])
            else:
                image = sysimage

            if 'banner' in i and not i['banner'] == '0':
                banner = i['banner']
            elif 'fanart' in i and not i['fanart'] == '0':
                banner = i['fanart']
            else:
                banner = image

            fanart = i['fanart'] if 'fanart' in i and not i['fanart'] == '0' else sysfanart

            isFolder = False if 'isFolder' in i and not i['isFolder'] == '0' else True

            try:
                is_play_boolean = i.get('isPlayable') in ['True', 'true', '1', 'yes', 'Yes']
            except Exception:
                is_play_boolean = False

            isPlayable = True if not isFolder and 'isPlayable' not in i else is_play_boolean

            if isPlayable:

                isFolder = False

            try:
                action = '{0}?action={1}'.format(sysaddon, i['action'])
            except KeyError:
                return

            try:
                url = 'url={0}'.format(quote_plus(i['url']))
            except Exception:
                url = None

            try:
                title = 'title={0}'.format(quote_plus(i['title']))
            except KeyError:
                try:
                    title = 'title={0}'.format(quote_plus(i['title'].encode('utf-8')))
                except KeyError:
                    title = None
            except Exception:
                title = None

            try:
                icon = 'image={0}'.format(quote_plus(i['image']))
            except KeyError:
                try:
                    icon = 'image={0}'.format(quote_plus(i['image'].encode('utf-8')))
                except KeyError:
                    icon = None
            except Exception:
                icon = None
            try:
                name = 'name={0}'.format(quote_plus(i['name']))
            except KeyError:
                try:
                    name = 'name={0}'.format(quote_plus(i['name'].encode('utf-8')))
                except KeyError:
                    name = None
            except Exception:
                name = None
            try:
                year = 'year={0}'.format(quote_plus(i['year']))
            except Exception:
                year = None
            try:
                plot = 'plot={0}'.format(quote_plus(i['plot']))
            except KeyError:
                try:
                    plot = 'plot={0}'.format(quote_plus(i['plot'].encode('utf-8')))
                except KeyError:
                    plot = None
            except Exception:
                plot = None
            try:
                genre = 'genre={0}'.format(quote_plus(i['genre']))
            except KeyError:
                try:
                    genre = 'genre={0}'.format(quote_plus(i['genre'].encode('utf-8')))
                except KeyError:
                    genre = None
            except Exception:
                genre = None
            try:
                dash = 'dash={0}'.format(quote_plus(i['dash']))
            except Exception:
                dash = None
            try:
                query = 'query={0}'.format(quote_plus(i['query']))
            except Exception:
                query = None

            parts = [foo for foo in [action, url, title, icon, name, year, plot, genre, dash, query] if foo]

            uri = '&'.join(parts)

            cm = []
            menus = i['cm'] if 'cm' in i else []

            for menu in menus:

                try:

                    try:
                        tmenu = control.lang(menu['title']).encode('utf-8')
                    except Exception:
                        tmenu = menu['title']
                    try:
                        qmenu = urlencode(menu['query'])
                    except Exception:
                        qmenu = urlencode(dict((k, v.encode('utf-8')) for k, v in menu['query'].items()))
                    cm.append((tmenu, 'RunPlugin({0}?{1})'.format(sysaddon, qmenu)))

                except Exception:

                    pass

            meta = dict((k, v) for k, v in iteritems(i) if not (k == 'cm' or k == 'streaminfo') and (not v == '0' or v is None))

            if mediatype is not None:
                meta['mediatype'] = mediatype

            item = control.item(label=label)

            item.setArt(
                {
                    'icon': image, 'thumb': image, 'poster': image, 'tvshow.poster': image, 'season.poster': image,
                    'banner': banner, 'tvshow.banner': banner, 'season.banner': banner, 'fanart': fanart
                }
            )

            item.addContextMenuItems(cm)
            item.setInfo(type=infotype, infoLabels=meta)

            if isPlayable:

                if not i['action'] == 'pvr_client':
                    item.setProperty('IsPlayable', 'true')
                else:
                    item.setProperty('IsPlayable', 'false')

                if not i['action'] == 'pvr_client':
                    if 'streaminfo' not in i and infotype == 'video':
                        item.addStreamInfo(infotype, {'codec': 'h264'})
                    else:
                        item.addStreamInfo(infotype, i.get('streaminfo'))

            if as_playlist and isPlayable:
                control.playlist(1 if infotype == 'video' else 0).add(url=uri, listitem=item, index=c)
            else:
                control.addItem(handle=syshandle, url=uri, listitem=item, isFolder=isFolder, totalItems=len(items))

        except Exception as reason:
            log('Directory not added, reason of failure: ' + repr(reason))

    if progress:
        pd.update(100)
        pd.close()

    if as_playlist:

        control.openPlaylist(1 if infotype == 'video' else 0)

        return

    try:

        i = items[0]
        if i['next'] == '':
            raise Exception()

        url = '{0}?action={1}&url={2}'.format(sysaddon, i['nextaction'], quote_plus(i['next']))
        icon = i['nexticon'] if 'nexticon' in i else control.addonmedia('next.png')
        fanart = i['nextfanart'] if 'nextfanart' in i else sysfanart

        try:
            label = control.lang(i['nextlabel']).encode('utf-8')
        except Exception:
            label = 'Next'

        item = control.item(label=label)

        item.setArt(
            {
                'icon': icon, 'thumb': icon, 'poster': icon, 'tvshow.poster': icon, 'season.poster': icon,
                'banner': icon, 'tvshow.banner': icon, 'season.banner': icon, 'fanart': fanart
            }
        )

        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True, totalItems=len(items))

    except Exception:

        pass

    if content is not None:
        control.content(syshandle, content)

    if category is not None:
        control.setcategory(syshandle, category)

    control.directory(syshandle, cacheToDisc=cacheToDisc)


def playlist_maker(items=None, argv=None):

    if items is None:
        return

    if argv is None:

        from tulip.init import sysaddon

    else:

        sysaddon = argv[0]

    m3u_list = [u'#EXTM3U\n']

    for i in items:

        try:
            action = '{0}?action={1}'.format(sysaddon, i['action'])
        except KeyError:
            return
        try:
            url = '&url={0}'.format(quote_plus(i['url']))
        except Exception:
            url = None
        try:
            title = '&title={0}'.format(quote_plus(i['title']))
        except KeyError:
            try:
                title = '&title={}'.format(quote_plus(i['title'].encode('utf-8')))
            except KeyError:
                title = None
        except Exception:
            title = None

        try:
            icon = '&image={0}'.format(quote_plus(i['image']))
        except KeyError:
            try:
                icon = '&image={0}'.format(quote_plus(i['image'].encode('utf-8')))
            except KeyError:
                icon = None
        except Exception:
            icon = None

        try:
            name = '&name={0}'.format(quote_plus(i['name']))
        except KeyError:
            try:
                name = '&name={0}'.format(quote_plus(i['name'].encode('utf-8')))
            except KeyError:
                name = None
        except Exception:
            name = None
        try:
            year = '&year={0}'.format(quote_plus(i['year']))
        except Exception:
            year = None
        try:
            plot = '&plot={0}'.format(quote_plus(i['plot']))
        except KeyError:
            try:
                plot = '&plot={0}'.format(quote_plus(i['plot'].encode('utf-8')))
            except KeyError:
                plot = None
        except Exception:
            plot = None

        parts = [foo for foo in [action, url, title, icon, name, year, plot] if foo]

        uri = '&'.join(parts)

        if icon:
            m3u_list.append(u'#EXTINF:0 tvg-logo="{0}",{1}\n'.format(icon, i['title']) + uri + '\n')
        else:
            m3u_list.append(u'#EXTINF:0,{0}\n'.format(i['title']) + uri + '\n')

    return ''.join(m3u_list)


def resolve(
        url, meta=None, icon=None, dash=False, manifest_type=None, inputstream_type='adaptive', headers=None,
        mimetype=None, resolved_mode=True, live=False
):

    """
    Prepares a resolved url into a listitem for playback

    :param url: Requires a string or unicode, append required urlencoded headers with pipe |
    :param meta: a dictionary with listitem keys: values
    :param icon: String
    :param dash: Boolean
    :param manifest_type: String
    :param inputstream_type: String 99.9% of the time it is adaptive
    :param headers: dictionary or urlencoded string
    :param mimetype: String
    :return: None
    """

    from tulip.init import syshandle

    # Fail gracefully instead of making Kodi complain.
    if url is None:
        from kodi_six.xbmc import log
        log('URL was not provided, failure to resolve stream')
        return

    if not headers and '|' in url:
        url = url.rpartition('|')[0]
        headers = url.rpartition('|')[2]
    elif headers:
        if isinstance(headers, basestring):
            if headers.startswith('|'):
                headers = headers[1:]
        elif isinstance(headers, dict):
            headers = urlencode(headers)

    if not dash and headers:
        url = '|'.join([url, headers])

    item = control.item(path=url)

    if icon is not None:
        item.setArt({'icon': icon, 'thumb': icon})

    if meta is not None:
        item.setInfo(type='Video', infoLabels=meta)

    krypton_plus = int(control.infoLabel('System.AddonVersion(xbmc.python)').replace('.', '')) >= 2250

    try:
        isa_enabled = control.addon_details('inputstream.adaptive').get('enabled')
    except KeyError:
        isa_enabled = False

    if dash and krypton_plus and isa_enabled:
        if not manifest_type:
            manifest_type = 'mpd'
        if not mimetype:
            mimetype = 'application/xml+dash'
        item.setContentLookup(False)
        item.setMimeType('{0}'.format(mimetype))
        item.setProperty('inputstreamaddon', 'inputstream.{}'.format(inputstream_type))
        item.setProperty('inputstream.{}.manifest_type'.format(inputstream_type), manifest_type)
        if headers:
            item.setProperty("inputstream.{}.stream_headers".format(inputstream_type), headers)
    elif mimetype:
        item.setContentLookup(False)
        item.setMimeType('{0}'.format(mimetype))

    if dash and live:
        item.setProperty('inputstream.{}.manifest_update_parameter'.format(inputstream_type), '&start_seq=$START_NUMBER$')

    if resolved_mode:
        control.resolve(syshandle, True, item)
    else:
        control.player().play(url, item)


def run_builtin(
        addon_id=control.addonInfo('id'), action=None, mode=None, content_type=None, url=None, query=None,
        path_history='', get_url=False, command=('ActivateWindow', 'Container.Update'), *args
):

    """
    This function will construct a url starting with plugin:// attached to the addon_id, then passed into either
    the ActivateWindow built-in command or Container.Update for listing/container manipulation. You have to either pass action,
    mode, content_type or query, otherwise TypeError will be raised. Can also apply the "PlayMedia".
    Query will override action, mode, url and content_type arguments if passed as dictionary
    path_history can also be either ",return" or ",replace"
    """

    if not query and not action and not mode and not content_type:

        raise TypeError('Cannot manipulate container without arguments')

    if isinstance(query, dict):

        query_string = urlencode(query)

    else:

        query_string = ''

        if content_type:
            query_string += 'content_type={0}{1}'.format(content_type, '&' if action is not None or mode is not None or query is not None else '')

        if action and not mode:
            query_string += 'action={0}'.format(action)
        elif mode and not action:
            query_string += 'mode={0}'.format(mode)
        else:
            query_string += 'action={0}&mode={1}'.format(action, mode)

        if url:
            query_string += '&url={0}'.format(quote_plus(url))

        if query:
            query_string += '&query={0}'.format(query)

        if args:
            query_string += '&' + '&'.join(args)

    if 'content_type=video' in query_string:
        window_id = 'videos'
    elif 'content_type=audio' in query_string:
        window_id = 'music'
    elif 'content_type=image' in query_string:
        window_id = 'pictures'
    elif 'content_type=executable' in query_string:
        window_id = 'programs'
    elif 'content_type' in query_string and dict(parse_qsl(query_string))['content_type'] not in ['video', 'audio', 'image', 'executable']:
        raise AttributeError('Incorrect content_type specified')

    addon_id = 'plugin://' + addon_id + '/'

    if 'content_type' in query_string and isinstance(command, tuple):

        # noinspection PyUnboundLocalVariable
        executable = '{0}({1},"{2}?{3}"{4})'.format(command[0], window_id, addon_id, query_string, ',return' if not path_history else path_history)

    else:

        if isinstance(command, tuple):

            executable = '{0}({1}?{2}{3})'.format(command[1], addon_id, query_string, ',return' if not path_history else path_history)

        else:

            executable = '{0}({1}?{2}{3})'.format(command, addon_id, query_string, ',return' if not path_history else path_history)

    if get_url:

        return executable

    else:

        control.execute(executable)


__all__ = ["add", "resolve", "playlist_maker", "run_builtin"]
