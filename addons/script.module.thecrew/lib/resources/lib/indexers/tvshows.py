# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    -Mofidied by The Crew
    -Copyright (C) 2019 The Crew


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from resources.lib.modules import trakt
from resources.lib.modules import cleantitle
from resources.lib.modules import cleangenre
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import metacache
from resources.lib.modules import playcount
from resources.lib.modules import workers
from resources.lib.modules import views
from resources.lib.modules import utils
from resources.lib.indexers import navigator

import os,sys,re,datetime
import simplejson as json
import six
from six.moves import urllib_parse, zip

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
import requests

params = dict(urllib_parse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

action = params.get('action')



class tvshows:
    def __init__(self):
        self.count = int(control.setting('page.item.limit'))
        self.list = []

        self.imdb_link = 'https://www.imdb.com'
        self.trakt_link = 'https://api.trakt.tv'
        self.tvmaze_link = 'https://www.tvmaze.com'
        self.logo_link = 'https://i.imgur.com/'
        self.tvdb_key = control.setting('tvdb.user')
        if self.tvdb_key == '' or self.tvdb_key == None:
            self.tvdb_key = '27bef29779bbffe947232dc310a91f0c'
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = control.setting('fanart.tv.user') + str('')
        self.lang = control.apiLanguage()['tvdb']

        self.search_link = 'https://api.trakt.tv/search/show?limit=20&page=1&query='
        self.tvmaze_info_link = 'https://api.tvmaze.com/shows/%s'
        self.tvdb_info_link = 'https://thetvdb.com/api/%s/series/%s/%s.zip.xml' % (self.tvdb_key, '%s', self.lang)
        self.fanart_tv_art_link = 'https://webservice.fanart.tv/v3/tv/%s'
        self.fanart_tv_level_link = 'https://webservice.fanart.tv/v3/level'
        self.tvdb_by_imdb = 'https://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
        self.tvdb_by_query = 'https://thetvdb.com/api/GetSeries.php?seriesname=%s'
        self.tvdb_image = 'https://thetvdb.com/banners/'

        self.imdb_link = 'http://www.imdb.com'
        self.persons_link = 'http://www.imdb.com/search/name?count=100&name='
        self.personlist_link = 'http://www.imdb.com/search/name?count=100&gender=male,female'
        self.popular_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=moviemeter,asc&count=%d&start=1' % self.count
        self.airing_link = 'http://www.imdb.com/search/title?title_type=tv_episode&release_date=date[1],date[0]&sort=moviemeter,asc&count=%d&start=1' % self.count
        self.active_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=10,&production_status=active&sort=moviemeter,asc&count=%d&start=1' % self.count
        self.premiere_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&languages=en&num_votes=10,&release_date=date[60],date[0]&sort=release_date,desc&count=%d&start=1' % self.count
        self.rating_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=5000,&release_date=,date[0]&sort=user_rating,desc&count=%d&start=1' % self.count
        self.views_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=num_votes,desc&count=%d&start=1' % self.count
        self.person_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&role=%s&sort=year,desc&count=%d&start=1' % ('%s', self.count)
        self.genre_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', self.count)
        self.keyword_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&keywords=%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', self.count)
        self.language_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', self.count)
        self.certification_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&certificates=%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', self.count)
        self.trending_link = 'https://api.trakt.tv/shows/trending?limit=40&page=1'

        self.traktlists_link = 'https://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'https://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link = 'https://api.trakt.tv/users/%s/lists/%s/items'
        self.traktcollection_link = 'https://api.trakt.tv/users/me/collection/shows'
        self.traktwatchlist_link = 'https://api.trakt.tv/users/me/watchlist/shows'
        self.traktfeatured_link = 'https://api.trakt.tv/recommendations/shows?limit=40'
        self.imdblists_link = 'https://www.imdb.com/user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'https://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=tvSeries,miniSeries&start=1'
        self.imdblist2_link = 'https://www.imdb.com/list/%s/?view=detail&sort=date_added,desc&title_type=tvSeries,miniSeries&start=1'
        self.imdbwatchlist_link = 'https://www.imdb.com/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user
        self.imdbwatchlist2_link = 'https://www.imdb.com/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user


    def get(self, url, idx=True, create_directory=True):
        try:
            try:
                url = getattr(self, url + '_link')
            except Exception:
                pass

            try:
                u = urllib_parse.urlparse(url).netloc.lower()
            except Exception:
                pass

            if u in self.trakt_link and '/users/' in url:
                try:
                    if '/users/me/' not in url:
                        raise Exception()
                    if trakt.getActivity() > cache.timeout(self.trakt_list, url, self.trakt_user):
                        raise Exception()
                    self.list = cache.get(self.trakt_list, 720, url, self.trakt_user)
                except Exception:
                    self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)

                if '/users/me/' in url and '/collection/' in url:
                    self.list = sorted(self.list, key=lambda k: utils.title_key(k['title']))

                if idx is True:
                    self.worker()

            elif u in self.trakt_link and self.search_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx is True:
                    self.worker(level=0)

            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx is True:
                    self.worker()
            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 0, url)
                if idx is True:
                    self.worker()
            elif u in self.imdb_link:
                self.list = cache.get(self.imdb_list, 24, url)
                if idx is True:
                    self.worker()
            elif u in self.tvmaze_link:
                self.list = cache.get(self.tvmaze_list, 168, url)
                if idx is True:
                    self.worker()

            if idx is True and create_directory is True:
                self.tvshowDirectory(self.list)
            return self.list
        except Exception:
            pass
#TC 2/01/19 started
    def search(self):
        navigator.navigator().addDirectoryItem(32603, 'tvSearchnew', 'search.png', 'DefaultTVShows.png')
        try:
            from sqlite3 import dbapi2 as database
        except Exception:
            from pysqlite2 import dbapi2 as database

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()

        try:
            dbcur.executescript("CREATE TABLE IF NOT EXISTS tvshow (ID Integer PRIMARY KEY AUTOINCREMENT, term);")
        except Exception:
            pass

        dbcur.execute("SELECT * FROM tvshow ORDER BY ID DESC")

        lst = []

        delete_option = False
        for (id, term) in dbcur.fetchall():
            if term not in str(lst):
                delete_option = True
                navigator.navigator().addDirectoryItem(term.title(), 'tvSearchterm&name=%s' % term, 'search.png', 'DefaultTVShows.png')
                lst += [(term)]
        dbcur.close()

        if delete_option:
            navigator.navigator().addDirectoryItem(32605, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')
        navigator.navigator().endDirectory()

    def search_new(self):
        control.idle()

        t = control.lang(32010)
        k = control.keyboard('', t)
        k.doModal()
        q = k.getText() if k.isConfirmed() else None

        if (q == None or q == ''):
            return
        q = q.lower()
        try:
            from sqlite3 import dbapi2 as database
        except Exception:
            from pysqlite2 import dbapi2 as database

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM tvshow WHERE term = ?", (q,))
        dbcur.execute("INSERT INTO tvshow VALUES (?,?)", (None, q))
        dbcon.commit()
        dbcur.close()
        url = self.search_link + urllib_parse.quote_plus(q)
        if control.getKodiVersion() >= 18:
            self.get(url)
        else:
            url = '%s?action=tvshowPage&url=%s' % (sys.argv[0], urllib_parse.quote_plus(url))
            control.execute('Container.Update(%s)' % url)

    def search_term(self, q):
        control.idle()
        q = q.lower()
        try:
            from sqlite3 import dbapi2 as database
        except Exception:
            from pysqlite2 import dbapi2 as database

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM tvshow WHERE term = ?", (q,))
        dbcur.execute("INSERT INTO tvshow VALUES (?,?)", (None, q))
        dbcon.commit()
        dbcur.close()
        url = self.search_link + urllib_parse.quote_plus(q)
        if control.getKodiVersion() >= 18:
            self.get(url)
        else:
            url = '%s?action=tvshowPage&url=%s' % (sys.argv[0], urllib_parse.quote_plus(url))
            control.execute('Container.Update(%s)' % url)

    def person(self):
        try:
            control.idle()

            t = control.lang(32010)
            k = control.keyboard('', t)
            k.doModal()
            q = k.getText() if k.isConfirmed() else None

            if (q == None or q == ''):
                return

            url = self.persons_link + urllib_parse.quote_plus(q)
            if control.getKodiVersion() >= 18:
                self.persons(url)
            else:
                url = '%s?action=tvPersons&url=%s' % (sys.argv[0], urllib_parse.quote_plus(url))
                control.execute('Container.Update(%s)' % url)
        except Exception:
            return

    def genres(self):
        genres = [
            ('Action', 'action', True),
            ('Adventure', 'adventure', True),
            ('Animation', 'animation', True),
            ('Anime', 'anime', False),
            ('Biography', 'biography', True),
            ('Comedy', 'comedy', True),
            ('Crime', 'crime', True),
            ('Drama', 'drama', True),
            ('Family', 'family', True),
            ('Fantasy', 'fantasy', True),
            ('Game-Show', 'game_show', True),
            ('History', 'history', True),
            ('Horror', 'horror', True),
            ('Music ', 'music', True),
            ('Musical', 'musical', True),
            ('Mystery', 'mystery', True),
            ('News', 'news', True),
            ('Reality-TV', 'reality_tv', True),
            ('Romance', 'romance', True),
            ('Science Fiction', 'sci_fi', True),
            ('Sport', 'sport', True),
            ('Talk-Show', 'talk_show', True),
            ('Thriller', 'thriller', True),
            ('War', 'war', True),
            ('Western', 'western', True)

        ]

        for i in genres: self.list.append(
            {
                'name': cleangenre.lang(i[0], self.lang),
                'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1],
                'image': 'genres2.png',
                'action': 'tvshows'
            })

        self.addDirectory(self.list)
        return self.list

    def networks(self):
        networks = [
        ('A&E', '/networks/29/ae', 'https://i.imgur.com/xLDfHjH.png'),
        ('ABC', '/networks/3/abc', 'https://i.imgur.com/qePLxos.png'),
        ('AMC', '/networks/20/amc', 'https://i.imgur.com/ndorJxi.png'),
        ('AT-X', '/networks/167/at-x', 'https://i.imgur.com/JshJYGN.png'),
        ('Adult Swim', '/networks/10/adult-swim', 'https://i.imgur.com/jCqbRcS.png'),
        ('Amazon', '/webchannels/3/amazon', 'https://i.imgur.com/ru9DDlL.png'),
        ('Animal Planet', '/networks/92/animal-planet', 'https://i.imgur.com/olKc4RP.png'),
        ('Audience', '/networks/31/audience-network', 'https://i.imgur.com/5Q3mo5A.png'),
        ('BBC America', '/networks/15/bbc-america', 'https://i.imgur.com/TUHDjfl.png'),
        ('BBC Four', '/networks/51/bbc-four', 'https://i.imgur.com/PNDalgw.png'),
        ('BBC One', '/networks/12/bbc-one', 'https://i.imgur.com/u8x26te.png'),
        ('BBC Three', '/webchannels/71/bbc-three', 'https://i.imgur.com/SDLeLcn.png'),
        ('BBC Two', '/networks/37/bbc-two', 'https://i.imgur.com/SKeGH1a.png'),
        ('BET', '/networks/56/bet', 'https://i.imgur.com/ZpGJ5UQ.png'),
        ('Bravo', '/networks/52/bravo', 'https://i.imgur.com/TmEO3Tn.png'),
        ('CBC', '/networks/36/cbc', 'https://i.imgur.com/unQ7WCZ.png'),
        ('CBS', '/networks/2/cbs', 'https://i.imgur.com/8OT8igR.png'),
        ('CTV', '/networks/48/ctv', 'https://i.imgur.com/qUlyVHz.png'),
        ('CW', '/networks/5/the-cw', 'https://i.imgur.com/Q8tooeM.png'),
        ('CW Seed', '/webchannels/13/cw-seed', 'https://i.imgur.com/nOdKoEy.png'),
        ('Cartoon Network', '/networks/11/cartoon-network', 'https://i.imgur.com/zmOLbbI.png'),
        ('Channel 4', '/networks/45/channel-4', 'https://i.imgur.com/6ZA9UHR.png'),
        ('Channel 5', '/networks/135/channel-5', 'https://i.imgur.com/5ubnvOh.png'),
        ('Cinemax', '/networks/19/cinemax', 'https://i.imgur.com/zWypFNI.png'),
        ('Comedy Central', '/networks/23/comedy-central', 'https://i.imgur.com/ko6XN77.png'),
        ('Crackle', '/webchannels/4/crackle', 'https://i.imgur.com/53kqZSY.png'),
        ('Discovery Channel', '/networks/66/discovery-channel', 'https://i.imgur.com/8UrXnAB.png'),
        ('Discovery ID', '/networks/89/investigation-discovery', 'https://i.imgur.com/07w7BER.png'),
        ('Disney Channel', '/networks/78/disney-channel', 'https://i.imgur.com/ZCgEkp6.png'),
        ('Disney +', '/webchannels/287/disney', 'https://static.tvmaze.com/uploads/images/large_landscape/174/435560.jpg'),
        ('Disney XD', '/networks/25/disney-xd', 'https://i.imgur.com/PAJJoqQ.png'),
        ('E! Entertainment', '/networks/43/e', 'https://i.imgur.com/3Delf9f.png'),
        ('E4', '/networks/41/e4', 'https://i.imgur.com/frpunK8.png'),
        ('FOX', '/networks/4/fox', 'https://i.imgur.com/6vc0Iov.png'),
        ('FX', '/networks/13/fx', 'https://i.imgur.com/aQc1AIZ.png'),
        ('Freeform', '/networks/26/freeform', 'https://i.imgur.com/f9AqoHE.png'),
        ('HBO', '/networks/8/hbo', 'https://i.imgur.com/Hyu8ZGq.png'),
        ('HGTV', '/networks/192/hgtv', 'https://i.imgur.com/INnmgLT.png'),
        ('Hallmark', '/networks/50/hallmark-channel', 'https://i.imgur.com/zXS64I8.png'),
        ('History Channel', '/networks/53/history', 'https://i.imgur.com/LEMgy6n.png'),
        ('Hulu', '/webchannels/2/hulu', 'https://i.imgur.com/uSD2Cdw.png'),
        ('ITV', '/networks/35/itv', 'https://i.imgur.com/5Hxp5eA.png'),
        ('Lifetime', '/networks/18/lifetime', 'https://i.imgur.com/tvYbhen.png'),
        ('MTV', '/networks/22/mtv', 'https://i.imgur.com/QM6DpNW.png'),
        ('NBC', '/networks/1/nbc', 'https://i.imgur.com/yPRirQZ.png'),
        ('National Geographic', '/networks/42/national-geographic-channel', 'https://i.imgur.com/XCGNKVQ.png'),
        ('Netflix', '/webchannels/1/netflix', 'https://i.imgur.com/jI5c3bw.png'),
        ('Nickelodeon', '/networks/27/nickelodeon', 'https://i.imgur.com/OUVoqYc.png'),
        ('PBS', '/networks/85/pbs', 'https://i.imgur.com/r9qeDJY.png'),
        ('Showtime', '/networks/9/showtime', 'https://i.imgur.com/SawAYkO.png'),
        ('Sky1', '/networks/63/sky-1', 'https://i.imgur.com/xbgzhPU.png'),
        ('Starz', '/networks/17/starz', 'https://i.imgur.com/Z0ep2Ru.png'),
        ('Sundance', '/networks/33/sundance-tv', 'https://i.imgur.com/qldG5p2.png'),
        ('Syfy', '/networks/16/syfy', 'https://i.imgur.com/9yCq37i.png'),
        ('TBS', '/networks/32/tbs', 'https://i.imgur.com/RVCtt4Z.png'),
        ('TLC', '/networks/80/tlc', 'https://i.imgur.com/c24MxaB.png'),
        ('TNT', '/networks/14/tnt', 'https://i.imgur.com/WnzpAGj.png'),
        ('TV Land', '/networks/57/tvland', 'https://i.imgur.com/1nIeDA5.png'),
        ('Travel Channel', '/networks/82/travel-channel', 'https://i.imgur.com/mWXv7SF.png'),
        ('TruTV', '/networks/84/trutv', 'https://i.imgur.com/HnB3zfc.png'),
        ('Youtube Red', '/webchannels/43/youtube-premium', 'https://i.imgur.com/ZfewP1Y.png'),
        ('USA', '/networks/30/usa-network', 'https://i.imgur.com/Doccw9E.png'),
        ('VH1', '/networks/55/vh1', 'https://i.imgur.com/IUtHYzA.png'),
        ('WGN', '/networks/28/wgn-america', 'https://i.imgur.com/TL6MzgO.png')
        ]

        for i in networks:
            self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': i[2], 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def languages(self):
        languages = [
            ('Arabic', 'ar'),
            ('Bosnian', 'bs'),
            ('Bulgarian', 'bg'),
            ('Chinese', 'zh'),
            ('Croatian', 'hr'),
            ('Dutch', 'nl'),
            ('English', 'en'),
            ('Finnish', 'fi'),
            ('French', 'fr'),
            ('German', 'de'),
            ('Greek', 'el'),
            ('Hebrew', 'he'),
            ('Hindi', 'hi'),
            ('Hungarian', 'hu'),
            ('Icelandic', 'is'),
            ('Italian', 'it'),
            ('Japanese', 'ja'),
            ('Korean', 'ko'),
            ('Norwegian', 'no'),
            ('Persian', 'fa'),
            ('Polish', 'pl'),
            ('Portuguese', 'pt'),
            ('Punjabi', 'pa'),
            ('Romanian', 'ro'),
            ('Russian', 'ru'),
            ('Serbian', 'sr'),
            ('Spanish', 'es'),
            ('Swedish', 'sv'),
            ('Turkish', 'tr'),
            ('Ukrainian', 'uk')
        ]

        for i in languages: self.list.append({'name': str(i[0]), 'url': self.language_link % i[1], 'image': 'international2.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def certifications(self):
        certificates = ['TV-G', 'TV-PG', 'TV-14', 'TV-MA']

        for i in certificates:
            self.list.append({'name': str(i), 'url': self.certification_link % str(i),
                'image': 'certificates.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def persons(self, url):
        if url is None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in list(range(0, len(self.list))):
            self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def userlists(self):
        try:
            userlists = []
            if trakt.getTraktCredentialsInfo() is False:
                raise Exception()
            activity = trakt.getActivity()
        except Exception:
            pass

        try:
            if trakt.getTraktCredentialsInfo() is False:
                raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link, self.trakt_user):
                    raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlists_link, self.trakt_user)
            except Exception:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
        except Exception:
            pass
        try:
            self.list = []
            if self.imdb_user == '':
                raise Exception()
            userlists += cache.get(self.imdb_user_list, 0, self.imdblists_link)
        except Exception:
            pass
        try:
            self.list = []
            if trakt.getTraktCredentialsInfo() is False:
                raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link, self.trakt_user):
                    raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlikedlists_link, self.trakt_user)
            except Exception:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)
        except Exception:
            pass
        self.list = userlists
        for i in list(range(0, len(self.list))):
            self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def trakt_list(self, url, user):
        try:
            dupes = []

            q = dict(urllib_parse.parse_qsl(urllib_parse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib_parse.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urllib_parse.urlparse(url).query, '') + '?' + q

            result = trakt.getTraktAsJson(u)

            items = []
            for i in result:
                try:
                    items.append(i['show'])
                except Exception:
                    pass
            if len(items) == 0:
                items = result
        except Exception:
            return

        try:
            q = dict(urllib_parse.parse_qsl(urllib_parse.urlsplit(url).query))
            if not int(q['limit']) == len(items):
                raise Exception()
            q.update({'page': str(int(q['page']) + 1)})
            q = (urllib_parse.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urllib_parse.urlparse(url).query, '') + '?' + q
            next = six.ensure_str(next)
        except Exception:
            next = ''

        for item in items:
            try:
                title = item['title']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = client.replaceHTMLCodes(title)

                year = item['year']
                year = re.sub('[^0-9]', '', str(year))

                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()

                imdb = item['ids']['imdb']
                if imdb is None or imdb == '':
                    imdb = '0'
                else:
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

                tvdb = item['ids']['tvdb']
                tvdb = re.sub('[^0-9]', '', str(tvdb))

                if tvdb is None or tvdb == '' or tvdb in dupes:
                    raise Exception()
                dupes.append(tvdb)

                try:
                    premiered = item['first_aired']
                except Exception:
                    premiered = '0'
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except Exception:
                    premiered = '0'

                try:
                    studio = item['network']
                except Exception:
                    studio = '0'
                if studio is None:
                    studio = '0'

                try:
                    genre = item['genres']
                except Exception:
                    genre = '0'
                genre = [i.title() for i in genre]
                if genre == []:
                    genre = '0'
                genre = ' / '.join(genre)

                try:
                    duration = str(item['runtime'])
                except Exception:
                    duration = '0'
                if duration is None:
                    duration = '0'

                try:
                    rating = str(item['rating'])
                except Exception:
                    rating = '0'
                if rating is None or rating == '0.0':
                    rating = '0'

                try:
                    votes = str(item['votes'])
                except Exception:
                    votes = '0'
                try:
                    votes = str(format(int(votes), ',d'))
                except Exception:
                    pass
                if votes is None:
                    votes = '0'

                try:
                    mpaa = item['certification']
                except Exception:
                    mpaa = '0'
                if mpaa is None:
                    mpaa = '0'

                try:
                    plot = item['overview']
                except Exception:
                    plot = '0'
                if plot is None:
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)

                self.list.append(
                    {'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': studio,
                     'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'plot': plot,
                     'imdb': imdb, 'tvdb': tvdb, 'poster': '0', 'next': next})
            except Exception:
                pass

        return self.list

    def trakt_user_list(self, url, user):
        try:
            items = trakt.getTraktAsJson(url)
        except Exception:
            pass

        for item in items:
            try:
                try:
                    name = item['list']['name']
                except Exception:
                    name = item['name']
                name = client.replaceHTMLCodes(name)

                try:
                    url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except Exception:
                    url = ('me', item['ids']['slug'])
                url = self.traktlist_link % url
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except Exception:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list

    def imdb_list(self, url):
        try:
            dupes = []

            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' %
                                  i, (self.datetime - datetime.timedelta(days=int(i))).strftime('%Y-%m-%d'))

            def imdb_watchlist_id(url):
                return client.parseDOM(client.request(url), 'meta', ret='content', attrs={'property': 'pageId'})[0]

            if url == self.imdbwatchlist_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url

            elif url == self.imdbwatchlist2_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist2_link % url

            result = client.request(url)
            result = control.six_decode(result)

            result = result.replace('\n', ' ')

            items = client.parseDOM(result, 'div', attrs={'class': 'lister-item .+?'})
            items += client.parseDOM(result, 'div', attrs={'class': 'list_item.+?'})
        except Exception:
            return

        try:
            next = client.parseDOM(result, 'a', ret='href', attrs={'class': 'lister-page-next .+?'})
            if len(next) == 0:
                next = client.parseDOM(result, 'a', ret='href', attrs={'class': '.+?lister-page-next .+?'})

            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs={'class': 'list-pagination'})[0]
                next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
                next = [i[0] for i in next if 'Next' in i[1]]

            next = url.replace(urllib_parse.urlparse(url).query, urllib_parse.urlparse(next[0]).query)
            next = client.replaceHTMLCodes(next)
            next = six.ensure_str(next)
        except Exception:
            next = ''

        for item in items:
            try:
                title = client.parseDOM(item, 'a')[1]
                title = client.replaceHTMLCodes(title)
                title = six.ensure_str(title)

                year = client.parseDOM(item, 'span', attrs={'class': 'lister-item-year.+?'})
                year += client.parseDOM(item, 'span', attrs={'class': 'year_type'})
                year = re.findall(r'(\d{4})', year[0])[0]
                year = six.ensure_str(year)

                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()

                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall('(tt\d*)', imdb)[0]
                imdb = six.ensure_str(imdb)

                if imdb in dupes:
                    raise Exception()
                dupes.append(imdb)

                try:
                    poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except Exception:
                    poster = '0'
                if '/nopicture/' in poster:
                    poster = '0'
                poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = six.ensure_str(poster)

                rating = '0'
                try:
                    rating = client.parseDOM(item, 'span', attrs={'class': 'rating-rating'})[0]
                except Exception:
                    pass
                try:
                    rating = client.parseDOM(rating, 'span', attrs={'class': 'value'})[0]
                except Exception:
                    rating = '0'
                try:
                    rating = client.parseDOM(item, 'div', ret='data-value', attrs={'class': '.*?imdb-rating'})[0]
                except Exception:
                    pass
                if rating == '' or rating == '-':
                    rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = six.ensure_str(rating)

                plot = '0'
                try:
                    plot = client.parseDOM(item, 'p', attrs={'class': 'text-muted'})[0]
                except Exception:
                    pass
                try:
                    plot = client.parseDOM(item, 'div', attrs={'class': 'item_description'})[0]
                except Exception:
                    pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                plot = re.sub('<.+?>|</.+?>', '', plot)
                if plot == '':
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = six.ensure_str(plot)

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'rating': rating,
                                  'plot': plot, 'imdb': imdb, 'tvdb': '0', 'poster': poster, 'next': next})
            except Exception:
                pass

        return self.list

    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'div', attrs={'class': '.+? mode-detail'})
        except Exception:
            return

        for item in items:
            try:
                name = client.parseDOM(item, 'img', ret='alt')[0]
                name = client.replaceHTMLCodes(name)
                name = six.ensure_str(name)

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall('(nm\d*)', url, re.I)[0]
                url = self.person_link % url
                url = client.replaceHTMLCodes(url)
                url = six.ensure_str(url)

                image = client.parseDOM(item, 'img', ret='src')[0]
                # if not ('._SX' in image or '._SY' in image): raise Exception()
                # image = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                image = client.replaceHTMLCodes(image)
                image = six.ensure_str(image)

                self.list.append({'name': name, 'url': url, 'image': image})
            except Exception:
                pass

        return self.list

    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'li', attrs={'class': 'ipl-zebra-list__item user-list'})
        except Exception:
            pass

        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = six.ensure_str(name)

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url = url.split('/list/', 1)[-1].strip('/')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = six.ensure_str(url)

                self.list.append({'name': name, 'url': url, 'context': url})
            except Exception:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list

    def tvmaze_list(self, url):
        try:
            result = client.request(url)
            result = client.parseDOM(result, 'section', attrs={'id': 'this-seasons-shows'})

            items = client.parseDOM(result, 'div', attrs={'class': 'content auto cell'})
            items = [client.parseDOM(i, 'a', ret='href') for i in items]
            items = [i[0] for i in items if len(i) > 0]
            items = [re.findall('/(\d+)/', i) for i in items]
            items = [i[0] for i in items if len(i) > 0]
            items = items[:50]
        except Exception:
            return

        def items_list(i):
            try:
                url = self.tvmaze_info_link % i

                item = requests.get(url, timeout=15, verify=True).json()
                #item = client.request(url)
                #item = json.loads(item)

                title = item['name']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = client.replaceHTMLCodes(title)
                title = six.ensure_str(title)

                year = item['premiered']
                year = re.findall('(\d{4})', year)[0]
                year = six.ensure_str(year)

                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()

                imdb = item['externals']['imdb']
                if imdb is None or imdb == '':
                    imdb = '0'
                else:
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = six.ensure_str(imdb)

                tvdb = item['externals']['thetvdb']
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = six.ensure_str(tvdb)

                if tvdb is None or tvdb == '':
                    raise Exception()

                try:
                    poster = item['image']['original']
                except Exception:
                    poster = '0'
                if poster is None or poster == '':
                    poster = '0'
                poster = six.ensure_str(poster)

                premiered = item['premiered']
                try:
                    premiered = re.findall('(\d{4}-\d{2}-\d{2})', premiered)[0]
                except Exception:
                    premiered = '0'
                premiered = six.ensure_str(premiered)

                try:
                    studio = item['network']['name']
                except Exception:
                    studio = '0'
                if studio is None:
                    studio = '0'
                studio = six.ensure_str(studio)

                try:
                    genre = item['genres']
                except Exception:
                    genre = '0'
                genre = [i.title() for i in genre]
                if genre == []:
                    genre = '0'
                genre = ' / '.join(genre)
                genre = six.ensure_str(genre)

                try:
                    duration = item['runtime']
                except Exception:
                    duration = '0'
                if duration is None:
                    duration = '0'
                duration = str(duration)
                duration = six.ensure_str(duration)

                try:
                    rating = item['rating']['average']
                except Exception:
                    rating = '0'
                if rating is None or rating == '0.0':
                    rating = '0'
                rating = str(rating)
                rating = six.ensure_str(rating)

                try:
                    plot = item['summary']
                except Exception:
                    plot = '0'
                if plot is None:
                    plot = '0'
                plot = re.sub('<.+?>|</.+?>|\n', '', plot)
                plot = client.replaceHTMLCodes(plot)
                plot = six.ensure_str(plot)

                try:
                    content = item['type'].lower()
                except Exception:
                    content = '0'
                if content is None or content == '':
                    content = '0'
                content = six.ensure_str(content)

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered,
                                  'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating,
                                  'plot': plot, 'imdb': imdb, 'tvdb': tvdb, 'poster': poster, 'content': content})
            except Exception:
                pass

        try:
            threads = []
            for i in items:
                threads.append(workers.Thread(items_list, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            filter = [i for i in self.list if i['content'] == 'scripted']
            filter += [i for i in self.list if not i['content'] == 'scripted']
            self.list = filter

            return self.list
        except Exception:
            return

    def worker(self, level=1):
        self.meta = []
        total = len(self.list)

        self.fanart_tv_headers = {'api-key': 'Nzk1ZjJhNjgwZmFiZmE2OTViNjE5MGNlNmY4ZmRlMGQ='.decode('base64')}
        if not self.fanart_tv_user == '':
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})

        for i in list(range(0, total)):
            self.list[i].update({'metacache': False})

        self.list = metacache.fetch(self.list, self.lang, self.user)

        for r in list(range(0, total, 40)):
            threads = []
            for i in list(range(r, r+40)):
                if i <= total:
                    threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            if self.meta:
                metacache.insert(self.meta)

        self.list = [i for i in self.list if not i['tvdb'] == '0']

        if self.fanart_tv_user == '':
            for i in self.list:
                i.update({'clearlogo': '0', 'clearart': '0'})

    def super_info(self, i):
        try:
            if self.list[i]['metacache'] is True:
                raise Exception()

            imdb = self.list[i]['imdb'] if 'imdb' in self.list[i] else '0'
            tvdb = self.list[i]['tvdb'] if 'tvdb' in self.list[i] else '0'

            if imdb == '0':
                try:
                    imdb = trakt.SearchTVShow(
                        urllib_parse.quote_plus(self.list[i]['title']),
                        self.list[i]['year'],
                        full=False)[0]
                    imdb = imdb.get('show', '0')
                    imdb = imdb.get('ids', {}).get('imdb', '0')
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

                    if not imdb:
                        imdb = '0'
                except Exception:
                    imdb = '0'

            if tvdb == '0' and not imdb == '0':
                url = self.tvdb_by_imdb % imdb

                #result = client.request(url, timeout='10')
                result = requests.get(url, timeout=10, verify=True).content
                result = control.six_decode(result)

                try:
                    tvdb = client.parseDOM(result, 'seriesid')[0]
                except Exception:
                    tvdb = '0'

                try:
                    name = client.parseDOM(result, 'SeriesName')[0]
                except Exception:
                    name = '0'
                dupe = re.findall('[***]Duplicate (\d*)[***]', name)
                if dupe:
                    tvdb = str(dupe[0])

                if tvdb == '':
                    tvdb = '0'

            if tvdb == '0':
                url = self.tvdb_by_query % (urllib_parse.quote_plus(self.list[i]['title']))

                years = [str(self.list[i]['year']), str(int(self.list[i]['year'])+1), str(int(self.list[i]['year'])-1)]

                #tvdb = client.request(url, timeout='10')
                tvdb = requests.get(url, timeout=10, verify=True).content
                tvdb = control.six_decode(tvdb)
                tvdb = re.sub(r'[^\x00-\x7F]+', '', tvdb)
                tvdb = client.replaceHTMLCodes(tvdb)
                tvdb = client.parseDOM(tvdb, 'Series')
                tvdb = [(x, client.parseDOM(x, 'SeriesName'), client.parseDOM(x, 'FirstAired')) for x in tvdb]
                tvdb = [(x, x[1][0], x[2][0]) for x in tvdb if len(x[1]) > 0 and len(x[2]) > 0]
                tvdb = [x for x in tvdb if cleantitle.get(self.list[i]['title']) == cleantitle.get(x[1])]
                tvdb = [x[0][0] for x in tvdb if any(y in x[2] for y in years)][0]
                tvdb = client.parseDOM(tvdb, 'seriesid')[0]

                if tvdb == '':
                    tvdb = '0'

            url = self.tvdb_info_link % tvdb
            item = requests.get(url, timeout=10, verify=True).content
            item = control.six_decode(item)
            if item is None:
                raise Exception()

            if imdb == '0':
                try:
                    imdb = client.parseDOM(item, 'IMDB_ID')[0]
                except Exception:
                    pass
                if imdb == '':
                    imdb = '0'
                imdb = six.ensure_str(imdb)

            try:
                title = client.parseDOM(item, 'SeriesName')[0]
            except Exception:
                title = ''
            if title == '':
                title = '0'
            title = client.replaceHTMLCodes(title)
            title = six.ensure_str(title)

            try:
                year = client.parseDOM(item, 'FirstAired')[0]
            except Exception:
                year = ''
            try:
                year = re.compile('(\d{4})').findall(year)[0]
            except Exception:
                year = ''
            if year == '':
                year = '0'
            year = six.ensure_str(year)

            try:
                premiered = client.parseDOM(item, 'FirstAired')[0]
            except Exception:
                premiered = '0'
            if premiered == '':
                premiered = '0'
            premiered = client.replaceHTMLCodes(premiered)
            premiered = six.ensure_str(premiered)

            try:
                studio = client.parseDOM(item, 'Network')[0]
            except Exception:
                studio = ''
            if studio == '':
                studio = '0'
            studio = client.replaceHTMLCodes(studio)
            studio = six.ensure_str(studio)

            try:
                genre = client.parseDOM(item, 'Genre')[0]
            except Exception:
                genre = ''
            genre = [x for x in genre.split('|') if not x == '']
            genre = ' / '.join(genre)
            if genre == '':
                genre = '0'
            genre = client.replaceHTMLCodes(genre)
            genre = six.ensure_str(genre)

            try:
                duration = client.parseDOM(item, 'Runtime')[0]
            except Exception:
                duration = ''
            if duration == '':
                duration = '0'
            duration = client.replaceHTMLCodes(duration)
            duration = six.ensure_str(duration)

            try:
                rating = client.parseDOM(item, 'Rating')[0]
            except Exception:
                rating = ''
            if 'rating' in self.list[i] and not self.list[i]['rating'] == '0':
                rating = self.list[i]['rating']
            if rating == '':
                rating = '0'
            rating = client.replaceHTMLCodes(rating)
            rating = six.ensure_str(rating)

            try:
                votes = client.parseDOM(item, 'RatingCount')[0]
            except Exception:
                votes = ''
            if 'votes' in self.list[i] and not self.list[i]['votes'] == '0':
                votes = self.list[i]['votes']
            if votes == '':
                votes = '0'
            votes = client.replaceHTMLCodes(votes)
            votes = six.ensure_str(votes)

            try:
                mpaa = client.parseDOM(item, 'ContentRating')[0]
            except Exception:
                mpaa = ''
            if mpaa == '':
                mpaa = '0'
            mpaa = client.replaceHTMLCodes(mpaa)
            mpaa = six.ensure_str(mpaa)

            try:
                cast = client.parseDOM(item, 'Actors')[0]
            except Exception:
                cast = ''
            cast = [x for x in cast.split('|') if not x == '']
            try:
                cast = [(six.ensure_str(x), '') for x in cast]
            except Exception:
                cast = []
            if cast == []:
                cast = '0'

            try:
                plot = client.parseDOM(item, 'Overview')[0]
            except Exception:
                plot = ''
            if plot == '':
                plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = six.ensure_str(plot)

            try:
                poster = client.parseDOM(item, 'poster')[0]
            except Exception:
                poster = ''
            if not poster == '':
                poster = self.tvdb_image + poster
            else:
                poster = '0'
            if 'poster' in self.list[i] and poster == '0':
                poster = self.list[i]['poster']
            poster = client.replaceHTMLCodes(poster)
            poster = six.ensure_str(poster)

            try:
                banner = client.parseDOM(item, 'banner')[0]
            except Exception:
                banner = ''
            if not banner == '':
                banner = self.tvdb_image + banner
            else:
                banner = '0'
            banner = client.replaceHTMLCodes(banner)
            banner = six.ensure_str(banner)

            try:
                fanart = client.parseDOM(item, 'fanart')[0]
            except Exception:
                fanart = ''
            if not fanart == '':
                fanart = self.tvdb_image + fanart
            else:
                fanart = '0'
            fanart = client.replaceHTMLCodes(fanart)
            fanart = six.ensure_str(fanart)

            try:
                artmeta = True
                # if self.fanart_tv_user == '': raise Exception()
                art = client.request(self.fanart_tv_art_link %
                                     tvdb, headers=self.fanart_tv_headers, timeout='10', error=True)
                try:
                    art = json.loads(art)
                except Exception:
                    artmeta = False
            except Exception:
                pass

            try:
                poster2 = art['tvposter']
                poster2 = [x for x in poster2 if x.get('lang') == self.lang][::-1] + [x for x in poster2 if x.get(
                    'lang') == 'en'][::-1] + [x for x in poster2 if x.get('lang') in ['00', '']][::-1]
                poster2 = six.ensure_str(poster2[0]['url'])
            except Exception:
                poster2 = '0'

            try:
                fanart2 = art['showbackground']
                fanart2 = [x for x in fanart2 if x.get('lang') == self.lang][::-1] + [x for x in fanart2 if x.get(
                    'lang') == 'en'][::-1] + [x for x in fanart2 if x.get('lang') in ['00', '']][::-1]
                fanart2 = six.ensure_str(fanart2[0]['url'])
            except Exception:
                fanart2 = '0'

            try:
                banner2 = art['tvbanner']
                banner2 = [x for x in banner2 if x.get('lang') == self.lang][::-1] + [x for x in banner2 if x.get(
                    'lang') == 'en'][::-1] + [x for x in banner2 if x.get('lang') in ['00', '']][::-1]
                banner2 = six.ensure_str(banner2[0]['url'])
            except Exception:
                banner2 = '0'

            try:
                if 'hdtvlogo' in art:
                    clearlogo = art['hdtvlogo']
                else:
                    clearlogo = art['clearlogo']
                clearlogo = [x for x in clearlogo if x.get('lang') == self.lang][::-1] + [x for x in clearlogo if x.get(
                    'lang') == 'en'][::-1] + [x for x in clearlogo if x.get('lang') in ['00', '']][::-1]
                clearlogo = six.ensure_str(clearlogo[0]['url'])
            except Exception:
                clearlogo = '0'

            try:
                if 'hdclearart' in art:
                    clearart = art['hdclearart']
                else:
                    clearart = art['clearart']
                clearart = [x for x in clearart if x.get('lang') == self.lang][::-1] + [x for x in clearart if x.get(
                    'lang') == 'en'][::-1] + [x for x in clearart if x.get('lang') in ['00', '']][::-1]
                clearart = six.ensure_str(clearart[0]['url'])
            except Exception:
                clearart = '0'

            item = {'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'poster': poster, 'poster2': poster2,
                    'banner': banner, 'banner2': banner2, 'fanart': fanart, 'fanart2': fanart2, 'clearlogo': clearlogo,
                    'clearart': clearart, 'premiered': premiered, 'studio': studio, 'genre': genre,
                    'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'cast': cast, 'plot': plot}
            item = dict((k,v) for k, v in six.iteritems(item) if not v == '0')
            self.list[i].update(item)

            if artmeta is False:
                raise Exception()

            meta = {'imdb': imdb, 'tvdb': tvdb, 'lang': self.lang, 'user': self.user, 'item': item}
            self.meta.append(meta)
        except:
            pass


    def tvshowDirectory(self, items):
        if items is None or len(items) == 0:
            control.idle()
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        traktCredentials = trakt.getTraktCredentialsInfo()

        try:
            isOld = False
            control.item().getArt('type')
        except Exception:
            isOld = True

        indicators = playcount.getTVShowIndicators(
            refresh=True) if action == 'tvshows' else playcount.getTVShowIndicators()
        flatten = True if control.setting('flatten.tvshows') == 'true' else False
        show_trailers = True if control.setting('showtrailers') == 'true' else False
        watchedMenu = control.lang(32068) if trakt.getTraktIndicatorsInfo() is True else control.lang(32066)
        unwatchedMenu = control.lang(32069) if trakt.getTraktIndicatorsInfo() is True else control.lang(32067)
        queueMenu = control.lang(32065)
        traktManagerMenu = control.lang(32070)
        nextMenu = control.lang(32053)
        playRandom = control.lang(32535)
        addToLibrary = control.lang(32551)

        infoMenu = control.lang(32101)
        for i in items:
            try:
                label = i['title']
                systitle = sysname = urllib_parse.quote_plus(i['originaltitle'])
                imdb, tvdb, year = i['imdb'], i['tvdb'], i['year']

                meta = dict((k, v) for k, v in six.iteritems(i) if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tvdb_id': tvdb})
                meta.update({'mediatype': 'tvshow'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib_parse.quote_plus(label))})
                if 'duration' not in i:
                    meta.update({'duration': '60'})
                elif i['duration'] == '0':
                    meta.update({'duration': '60'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except Exception:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except Exception:
                    pass

                try:
                    overlay = int(playcount.getTVShowOverlay(indicators, tvdb))
                    if overlay == 7:
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        meta.update({'playcount': 0, 'overlay': 6})
                except Exception:
                    pass

                if flatten is True:
                    url = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s' % (
                        sysaddon, systitle, year, imdb, tvdb)
                else:
                    url = '%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s' % (
                        sysaddon, systitle, year, imdb, tvdb)

                cm = []

                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=season&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s)' % (
                    sysaddon, urllib_parse.quote_plus(systitle), urllib_parse.quote_plus(year), urllib_parse.quote_plus(imdb), urllib_parse.quote_plus(tvdb))))

                if show_trailers is True:
                    cm.append(('Watch Trailer', 'RunPlugin(%s?action=trailer&name=%s)' % (sysaddon, urllib_parse.quote_plus(label))))

                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                cm.append(
                    (watchedMenu, 'RunPlugin(%s?action=tvPlaycount&name=%s&imdb=%s&tvdb=%s&query=7)' %
                     (sysaddon, systitle, imdb, tvdb)))
                cm.append(
                    (unwatchedMenu, 'RunPlugin(%s?action=tvPlaycount&name=%s&imdb=%s&tvdb=%s&query=6)' %
                     (sysaddon, systitle, imdb, tvdb)))

                if traktCredentials is True:
                    cm.append(
                        (traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&tvdb=%s&content=tvshow)' %
                         (sysaddon, sysname, tvdb)))

                if isOld == True:
                    cm.append((infoMenu, 'Action(Info)'))

                cm.append(
                    (addToLibrary, 'RunPlugin(%s?action=tvshowToLibrary&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s)' %
                     (sysaddon, systitle, year, imdb, tvdb)))

                item = control.item(label=label)

                art = {}

                if 'poster' in i and not i['poster'] == '0':
                    art.update({'icon': i['poster'], 'thumb': i['poster'], 'poster': i['poster']})
                #elif 'poster2' in i and not i['poster2'] == '0':
                    #art.update({'icon': i['poster2'], 'thumb': i['poster2'], 'poster': i['poster2']})
                else:
                    art.update({'icon': addonPoster, 'thumb': addonPoster, 'poster': addonPoster})

                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                #elif 'banner2' in i and not i['banner2'] == '0':
                    #art.update({'banner': i['banner2']})
                elif 'fanart' in i and not i['fanart'] == '0':
                    art.update({'banner': i['fanart']})
                else:
                    art.update({'banner': addonBanner})

                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})

                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})

                if settingFanart == 'true' and 'fanart' in i and not i['fanart'] == '0':
                    item.setProperty('Fanart_Image', i['fanart'])
                #elif settingFanart == 'true' and 'fanart2' in i and not i['fanart2'] == '0':
                    #item.setProperty('Fanart_Image', i['fanart2'])
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setInfo(type='Video', infoLabels=control.metadataClean(meta))

                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        try:
            url = items[0]['next']
            if url == '': raise Exception()

            icon = control.addonNext()
            url = '%s?action=tvshowPage&url=%s' % (sysaddon, urllib_parse.quote_plus(url))

            item = control.item(label=nextMenu)

            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass

        control.content(syshandle, 'tvshows')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('tvshows', {'skin.estuary': 55, 'skin.confluence': 500})


    def addDirectory(self, items, queue=False):
        if items is None or len(items) == 0:
            control.idle()
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()
        queueMenu = control.lang(32065)
        playRandom = control.lang(32535)
        addToLibrary = control.lang(32551)

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif artPath is not None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try:
                    url += '&url=%s' % urllib_parse.quote_plus(i['url'])
                except Exception:
                    pass

                cm = []
                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=show&url=%s)' %
                           (sysaddon, urllib_parse.quote_plus(i['url']))))

                if queue is True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    cm.append((addToLibrary, 'RunPlugin(%s?action=tvshowsToLibrary&url=%s)' %
                               (sysaddon, urllib_parse.quote_plus(i['context']))))
                except Exception:
                    pass

                item = control.item(label=name)

                item.setArt({'icon': thumb, 'thumb': thumb})
                if addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except Exception:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)