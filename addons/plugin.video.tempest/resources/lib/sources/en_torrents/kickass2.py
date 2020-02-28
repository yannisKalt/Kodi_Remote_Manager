# -*- coding: utf-8 -*-
# -Cleaned and Checked on 02-24-2019 by JewBMX in Scrubs.
# -Fixed by Tempest on 09-08-2019

import re,urllib,urlparse
import traceback
from resources.lib.modules import client,cleantitle,debrid,source_utils,workers,control
from resources.lib.modules import log_utils, control
from resources.lib.modules import cache_check
from resources.lib.sources import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['kickass2.cc']
        self.base_link = 'https://thekat.nl/'
        self.search = 'https://thekat.nl/usearch/{0}'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            self._sources = []
            self.items = []
            if url is None:
                return self._sources
            if debrid.status() is False:
                raise Exception()
            if debrid.torrent_enabled() is False:
                raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s S%02dE%02d' % (
            data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
            data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            url = self.search.format(urllib.quote(query))
            self._get_items(url)
            self.hostDict = hostDict + hostprDict
            threads = []
            for i in self.items:
                threads.append(workers.Thread(self._get_sources, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            return self._sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Kickass2 Testing - Exception: \n' + str(failure))
            return self._sources

    def _get_items(self, url):
        try:
            headers = {'User-Agent': client.agent()}
            r = cfscrape.get(url).content
            posts = client.parseDOM(r, 'tr', attrs={'id': 'torrent_latest_torrents'})
            for post in posts:
                data = client.parseDOM(post, 'a', attrs={'title': 'Torrent magnet link'}, ret='href')[0]
                link = urllib.unquote(data).decode('utf8').replace('https://mylink.me.uk/?url=', '')
                name = urllib.unquote_plus(re.search('dn=([^&]+)', link).groups()[0])
                t = name.split(self.hdlr)[0]
                if not cleantitle.get(re.sub('(|)', '', t)) == cleantitle.get(self.title): continue
                try:
                    y = re.findall('[\.|\(|\[|\s|\_|\-](S\d+E\d+|S\d+)[\.|\)|\]|\s|\_|\-]', name, re.I)[-1].upper()
                except BaseException:
                    y = re.findall('[\.|\(|\[|\s\_|\-](\d{4})[\.|\)|\]|\s\_|\-]', name, re.I)[-1].upper()
                if not y == self.hdlr: continue
                try:
                    size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', post)[0]
                    div = 1 if size.endswith('GB') else 1024
                    size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                    size = '%.2f GB' % size
                except BaseException:
                    size = '0'
                self.items.append((name, link, size))
            return self.items
        except BaseException:
            return self.items

    def _get_sources(self, item):
        try:
            name = item[0]
            url = item[1]
            url = url.split('&tr')[0]
            url = url.split('url=')[1]
            if any(x in url for x in ['FRENCH', 'Ita', 'ITA', 'italian', 'Tamil', 'TRUEFRENCH', '-lat-', 'Dublado', 'Dub', 'Rus', 'Hindi']):
                raise Exception
            quality, info = source_utils.get_release_quality(url, name)
            info.append(item[2])
            info = ' | '.join(info)
            if control.setting('torrent.cache_check') == 'true':
                cached = cache_check.rd_cache_check(url)
                if not cached:
                    raise Exception()
                self._sources.append(
                    {'source': 'Cached Torrent', 'quality': quality, 'language': 'en', 'url': url,'info': info,
                     'direct': False, 'debridonly': True})
            else:
                self._sources.append(
                    {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                     'direct': False, 'debridonly': True})
        except BaseException:
            pass

    def resolve(self, url):
        return url
