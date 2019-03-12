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

from xbmc import getCleanMovieTitle

import re
from resources.lib import subtitlesgr, xsubstv, subzxyz
from resources.lib.tools import syshandle, sysaddon, langs

from tulip import control, workers, log
from tulip.compat import urlencode, range


class Search:

    def __init__(self):

        self.list = []
        self.query = None

    def run(self, query=None):

        if not 'Greek' in str(langs).split(','):

            control.directory(syshandle)
            control.infoDialog(control.lang(32002))

            return

        threads = [workers.Thread(self.xsubstv), workers.Thread(self.subzxyz), workers.Thread(self.subtitlesgr)]
        dup_removal = False

        if not query:

            if control.condVisibility('Player.HasVideo'):
                infolabel_prefix = 'VideoPlayer'
            else:
                infolabel_prefix = 'ListItem'

            title = control.infoLabel('{0}.Title'.format(infolabel_prefix))

            if re.search(r'[^\x00-\x7F]+', title) is not None:

                title = control.infoLabel('{0}.OriginalTitle'.format(infolabel_prefix))

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
                    workers.Thread(self.xsubstv, title_query), workers.Thread(self.subzxyz, title_query),
                    workers.Thread(self.subtitlesgr, title_query), workers.Thread(self.xsubstv, season_episode_query),
                    workers.Thread(self.subzxyz, season_episode_query), workers.Thread(self.subtitlesgr, season_episode_query)
                ]
                dup_removal = True
                log.log('Dual query used for subtitles search: ' + title_query + ' / ' + season_episode_query)
            elif year != '':  # movie
                query = '{0} ({1})'.format(title, year)
            else:  # file
                query, year = getCleanMovieTitle(title)
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

            control.sleep(750)

        if len(self.list) == 0:

            control.directory(syshandle)
            control.infoDialog(control.lang(32218), time=6000)

            return

        f = []

        # noinspection PyUnresolvedReferences
        f += [i for i in self.list if i['source'] == 'xsubstv']
        f += [i for i in self.list if i['source'] == 'subzxyz']
        f += [i for i in self.list if i['source'] == 'subtitlesgr']

        self.list = f

        if dup_removal:

            self.list = [dict(t) for t in {tuple(d.items()) for d in self.list}]

        for i in self.list:

            try:

                if i['source'] == 'subzxyz':
                    i['name'] = '[subzxyz] {0}'.format(i['name'])
                elif i['source'] == 'xsubstv':
                    i['name'] = '[xsubstv] {0}'.format(i['name'])

            except Exception:

                pass

        for i in self.list:

            u = {'action': 'download', 'url': i['url'], 'source': i['source']}
            u = '{0}?{1}'.format(sysaddon, urlencode(u))

            item = control.item(label='Greek', label2=i['name'], iconImage=str(i['rating']), thumbnailImage='el')
            item.setProperty('sync', 'false')
            item.setProperty('hearing_imp', 'false')

            control.addItem(handle=syshandle, url=u, listitem=item, isFolder=False)

        control.directory(syshandle)

    def subtitlesgr(self, query=None):

        if not query:

            query = self.query

        try:
            self.list.extend(subtitlesgr.subtitlesgr().get(query))
        except TypeError:
            pass

    def xsubstv(self, query=None):

        if not query:

            query = self.query

        try:

            self.list.extend(xsubstv.xsubstv().get(query))

        except TypeError:

            pass

    def subzxyz(self, query=None):

        if not query:

            query = self.query

        try:

            self.list.extend(subzxyz.subzxyz().get(query))

        except TypeError:

            pass


class Download:

    def __init__(self):

        pass

    def run(self, url, source):

        path = control.join(control.dataPath, 'temp')

        try:

            path = path.decode('utf-8')

        except Exception:

            pass

        control.deleteDir(control.join(path, ''), force=True)

        control.makeFile(control.dataPath)

        control.makeFile(path)

        if source == 'subtitlesgr':

            subtitle = subtitlesgr.subtitlesgr().download(path, url)

        elif source == 'xsubstv':

            subtitle = xsubstv.xsubstv().download(path, url)

        elif source == 'subzxyz':

            subtitle = subzxyz.subzxyz().download(path, url)

        elif source == 'tvsubtitlesgr':

            subtitle = None

        else:

            subtitle = None

        if subtitle is not None:

            item = control.item(label=subtitle)
            control.addItem(handle=syshandle, url=subtitle, listitem=item, isFolder=False)

        control.directory(syshandle)
