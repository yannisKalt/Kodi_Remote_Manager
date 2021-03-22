# -*- coding: utf-8 -*-

'''
    Subtitles.gr Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import re, unicodedata
from shutil import copy
from os.path import split as os_split
from resources.lib import subtitlesgr, xsubstv, podnapisi, vipsubs

from tulip import workers, cache, control
from tulip.compat import urlencode, range
from tulip.log import log_debug


class Search:

    def __init__(self, syshandle, sysaddon, langs, action):

        self.list = []
        self.query = None
        self.syshandle = syshandle
        self.sysaddon = sysaddon
        self.langs = langs
        self.action = action

    def run(self, query=None):

        if 'Greek' not in str(self.langs).split(','):

            control.directory(self.syshandle)
            control.infoDialog(control.lang(30002))

            return

        if control.kodi_version() >= 18.0 and not control.conditional_visibility('System.HasAddon(vfs.libarchive)') and not (
            control.condVisibility('System.Platform.Linux')
        ):
            control.execute('InstallAddon(vfs.libarchive)')

        threads = [
            workers.Thread(self.xsubstv), workers.Thread(self.subtitlesgr), workers.Thread(self.podnapisi),
            workers.Thread(self.vipsubs)
        ]

        dup_removal = False

        if not query:

            if control.condVisibility('Player.HasVideo'):
                infolabel_prefix = 'VideoPlayer'
            else:
                infolabel_prefix = 'ListItem'

            title = control.infoLabel('{0}.Title'.format(infolabel_prefix))

            if re.search(r'[^\x00-\x7F]+', title) is not None:

                title = control.infoLabel('{0}.OriginalTitle'.format(infolabel_prefix))

            title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore')

            year = control.infoLabel('{0}.Year'.format(infolabel_prefix))

            tvshowtitle = control.infoLabel('{0}.TVshowtitle'.format(infolabel_prefix))

            season = control.infoLabel('{0}.Season'.format(infolabel_prefix))

            if len(season) == 1:

                season = '0' + season

            episode = control.infoLabel('{0}.Episode'.format(infolabel_prefix))

            if len(episode) == 1:
                episode = '0' + episode

            if 's' in episode.lower():
                season, episode = '0', episode[-1:]

            if tvshowtitle != '':  # episode

                title_query = '{0} {1}'.format(tvshowtitle, title)
                season_episode_query = '{0} S{1} E{2}'.format(tvshowtitle, season, episode)
                season_episode_query_nospace = '{0} S{1}E{2}'.format(tvshowtitle, season, episode)

                threads = [
                    workers.Thread(self.subtitlesgr, season_episode_query_nospace),
                    workers.Thread(self.xsubstv, season_episode_query),
                    workers.Thread(self.podnapisi, season_episode_query),
                    workers.Thread(self.vipsubs, season_episode_query)
                ]

                if control.setting('queries') == 'true':

                    threads.extend(
                        [
                            workers.Thread(self.subtitlesgr, title_query),workers.Thread(self.vipsubs, title_query),
                            workers.Thread(self.podnapisi, title_query), workers.Thread(self.subtitlesgr, season_episode_query)
                        ]
                    )

                    dup_removal = True

                    log_debug('Dual query used for subtitles search: ' + title_query + ' / ' + season_episode_query)

            elif year != '':  # movie

                query = '{0} ({1})'.format(title, year)

            else:  # file

                query, year = control.cleanmovietitle(title)

                if year != '':

                    query = '{0} ({1})'.format(query, year)

        if not dup_removal:

            log_debug('Query used for subtitles search: ' + query)

        self.query = query

        [i.start() for i in threads]

        for i in range(0, 40):

            is_alive = [x.is_alive() for x in threads]

            if all(not x for x in is_alive):
                log_debug('Counted results: ' + str(i))
                break
            if control.aborted is True:
                log_debug('Aborted, reached count : ' + str(i))
                break

            control.sleep(400)

        if len(self.list) == 0:

            control.directory(self.syshandle)

            return

        f = []

        # noinspection PyUnresolvedReferences
        f += [i for i in self.list if i['source'] == 'xsubstv']
        f += [i for i in self.list if i['source'] == 'subtitlesgr']
        f += [i for i in self.list if i['source'] == 'podnapisi']
        f += [i for i in self.list if i['source'] == 'vipsubs']

        self.list = f

        if dup_removal:

            self.list = [dict(t) for t in {tuple(d.items()) for d in self.list}]

        for i in self.list:

            try:

                if i['source'] == 'xsubstv':
                    i['name'] = u'[xsubstv] {0}'.format(i['name'])
                elif i['source'] == 'podnapisi':
                    i['name'] = u'[podnapisi] {0}'.format(i['name'])
                elif i['source'] == 'vipsubs':
                    i['name'] = u'[vipsubs] {0}'.format(i['name'])

            except Exception:

                pass

        if control.setting('sorting') == '1':
            key = 'source'
        elif control.setting('sorting') == '2':
            key = 'downloads'
        elif control.setting('sorting') == '3':
            key = 'rating'
        else:
            key = 'title'

        self.list = sorted(self.list, key=lambda k: k[key].lower(), reverse=control.setting('sorting') in ['1', '2', '3'])

        for i in self.list:

            u = {'action': 'download', 'url': i['url'], 'source': i['source']}
            u = '{0}?{1}'.format(self.sysaddon, urlencode(u))

            item = control.item(label='Greek', label2=i['name'], iconImage=str(i['rating'])[:1], thumbnailImage='el')
            item.setProperty('sync', 'false')
            item.setProperty('hearing_imp', 'false')

            control.addItem(handle=self.syshandle, url=u, listitem=item, isFolder=False)

        control.directory(self.syshandle)

    def subtitlesgr(self, query=None):

        if not query:

            query = self.query

        try:

            if control.setting('subtitles') == 'false':
                raise TypeError

            if control.setting('cache') == 'true':
                result = cache.get(subtitlesgr.Subtitlesgr().get, 2, query)
            else:
                result = subtitlesgr.Subtitlesgr().get(query)

            self.list.extend(result)

        except TypeError:

            pass

    def podnapisi(self, query=None):

        if not query:

            query = self.query

        try:

            if control.setting('podnapisi') == 'false':
                raise TypeError

            if control.setting('cache') == 'true':
                result = cache.get(podnapisi.Podnapisi().get, 2, query)
            else:
                result = podnapisi.Podnapisi().get(query)

            self.list.extend(result)

        except TypeError:

            pass

    def vipsubs(self, query=None):

        if not query:

            query = self.query

        try:

            if control.setting('vipsubs') == 'false':
                raise TypeError

            if control.setting('cache') == 'true':
                result = cache.get(vipsubs.Vipsubs().get, 2, query)
            else:
                result = vipsubs.Vipsubs().get(query)

            self.list.extend(result)

        except TypeError:

            pass

    def xsubstv(self, query=None):

        if not query:

            query = self.query

        try:

            if control.setting('xsubs') == 'false':
                raise TypeError

            if control.setting('cache') == 'true':
                result = cache.get(xsubstv.Xsubstv().get, 2, query)
            else:
                result = xsubstv.Xsubstv().get(query)

            self.list.extend(result)

        except TypeError:

            pass


class Download:

    def __init__(self, syshandle, sysaddon):

        self.syshandle = syshandle
        self.sysaddon = sysaddon

    def run(self, url, source):

        log_debug('Source selected: {0}'.format(source))

        path = control.join(control.dataPath, 'temp')

        try:

            path = path.decode('utf-8')

        except Exception:

            pass

        control.deleteDir(control.join(path, ''), force=True)

        control.makeFile(control.dataPath)

        control.makeFile(path)

        if control.setting('keep_subs') == 'true' or control.setting('keep_zips') == 'true':

            if control.setting('output_folder').startswith('special://'):
                output_path = control.transPath(control.setting('output_folder'))
            else:
                output_path = control.setting('output_folder')

            control.makeFile(output_path)

        if source == 'subtitlesgr':

            subtitle = subtitlesgr.Subtitlesgr().download(path, url)

        elif source == 'xsubstv':

            subtitle = xsubstv.Xsubstv().download(path, url)

        elif source == 'podnapisi':

            subtitle = podnapisi.Podnapisi().download(path, url)

        elif source == 'vipsubs':

            subtitle = vipsubs.Vipsubs().download(path, url)

        else:

            subtitle = None

        if subtitle is not None:

            if control.setting('keep_subs') == 'true':

                # noinspection PyUnboundLocalVariable
                copy(subtitle, control.join(output_path, os_split(subtitle)[1]))
                control.infoDialog(control.lang(30008))

            item = control.item(label=subtitle)
            control.addItem(handle=self.syshandle, url=subtitle, listitem=item, isFolder=False)

        control.directory(self.syshandle)
