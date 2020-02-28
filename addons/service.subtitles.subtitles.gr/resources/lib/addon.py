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

import re, unicodedata
from resources.lib import subtitlesgr, xsubstv, podnapisi, subs4free
from resources.lib.tools import syshandle, sysaddon, langs

from tulip import control, workers, log, cache
from tulip.compat import urlencode, range


class Search:

    def __init__(self):

        self.list = []
        self.query = None

    def run(self, query=None):

        if 'Greek' not in str(langs).split(','):

            control.directory(syshandle)
            control.infoDialog(control.lang(32002))

            return

        if not control.conditional_visibility(
            'System.HasAddon(vfs.libarchive)'
        ) and float(
            control.addon('xbmc.addon').getAddonInfo('version')[:4]
        ) >= 18.0 and not (
            control.condVisibility('System.Platform.Linux') or control.condVisibility('System.Platform.Linux.RaspberryPi')
        ):

            control.execute('InstallAddon(vfs.libarchive)')

        threads = [
            workers.Thread(self.xsubstv), workers.Thread(self.subtitlesgr), workers.Thread(self.podnapisi),
            workers.Thread(self.subs4free)
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

                threads = [
                    workers.Thread(self.subtitlesgr, title_query), workers.Thread(self.subtitlesgr, season_episode_query),
                    workers.Thread(self.xsubstv, season_episode_query), workers.Thread(self.podnapisi, title_query),
                    workers.Thread(self.podnapisi, season_episode_query), workers.Thread(self.subs4free, title_query),
                    workers.Thread(self.subs4free, season_episode_query)
                ]

                dup_removal = True
                log.log('Dual query used for subtitles search: ' + title_query + ' / ' + season_episode_query)

            elif year != '':  # movie

                query = '{0} ({1})'.format(title, year)

            else:  # file

                query, year = control.cleanmovietitle(title)

                if year != '':

                    query = '{0} ({1})'.format(query, year)

        if not dup_removal:

            log.log('Query used for subtitles search: ' + query)

        self.query = query

        [i.start() for i in threads]

        for c, i in list(enumerate(range(0, 40))):

            is_alive = [x.is_alive() for x in threads]

            if all(x is False for x in is_alive):
                log.log('Reached count : ' + str(c))
                break
            if control.aborted is True:
                log.log('Aborted, reached count : ' + str(c))
                break

            control.sleep(200)

        if len(self.list) == 0:

            control.directory(syshandle)

            return

        f = []

        # noinspection PyUnresolvedReferences
        f += [i for i in self.list if i['source'] == 'xsubstv']
        f += [i for i in self.list if i['source'] == 'subtitlesgr']
        f += [i for i in self.list if i['source'] == 'podnapisi']
        f += [i for i in self.list if i['source'] == 'subs4free']

        self.list = f

        if dup_removal:

            self.list = [dict(t) for t in {tuple(d.items()) for d in self.list}]

        for i in self.list:

            try:

                if i['source'] == 'xsubstv':
                    i['name'] = u'[xsubstv] {0}'.format(i['name'])
                elif i['source'] == 'podnapisi':
                    i['name'] = u'[podnapisi] {0}'.format(i['name'])
                elif i['source'] == 'subs4free':
                    i['name'] = u'[subs4free] {0}'.format(i['name'])

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
            u = '{0}?{1}'.format(sysaddon, urlencode(u))

            item = control.item(label='Greek', label2=i['name'], iconImage=str(i['rating'])[:1], thumbnailImage='el')
            item.setProperty('sync', 'false')
            item.setProperty('hearing_imp', 'false')

            control.addItem(handle=syshandle, url=u, listitem=item, isFolder=False)

        control.directory(syshandle)

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

    def subs4free(self, query=None):

        if not query:

            query = self.query

        try:

            if control.setting('subs4free') == 'false':
                raise TypeError

            if control.setting('cache') == 'true':
                result = cache.get(subs4free.Subs4free().get, 2, query)
            else:
                result = subs4free.Subs4free().get(query)

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

    def __init__(self):

        pass

    @staticmethod
    def run(url, source):

        path = control.join(control.dataPath, 'temp')

        try:

            path = path.decode('utf-8')

        except Exception:

            pass

        control.deleteDir(control.join(path, ''), force=True)

        control.makeFile(control.dataPath)

        control.makeFile(path)

        if source == 'subtitlesgr':

            subtitle = subtitlesgr.Subtitlesgr().download(path, url)

        elif source == 'xsubstv':

            subtitle = xsubstv.Xsubstv().download(path, url)

        elif source == 'podnapisi':

            subtitle = podnapisi.Podnapisi().download(path, url)

        elif source == 'subs4free':

            subtitle = subs4free.Subs4free().download(path, url)

        else:

            subtitle = None

        if subtitle is not None:

            item = control.item(label=subtitle)
            control.addItem(handle=syshandle, url=subtitle, listitem=item, isFolder=False)

        control.directory(syshandle)
