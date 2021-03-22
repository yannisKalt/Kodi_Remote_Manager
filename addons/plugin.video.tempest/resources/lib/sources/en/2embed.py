# -*- coding: utf-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import scrape_source


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['2embed.ru']
        self.base_link = 'https://www.2embed.ru'
        self.search_link = '/embed/imdb/movie?id=%s'
        self.search_link2 = '/embed/imdb/tv?id=%s'
        self.headers = {'User-Agent': client.agent(), 'Referer': self.base_link}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            items = []

            if url is None:
                return sources

            hostDict = hostprDict + hostDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = '%s&s=%s&e=%s' % (
            data['imdb'], data['season'], data['episode']) if 'tvshowtitle' in data else '%s' % (data['imdb'])
            query = re.sub('(\\\|/| -|:|\.|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            if 'tvshowtitle' in data:
                url = self.search_link2 % query
            else:
                url = self.search_link % query
            url = urlparse.urljoin(self.base_link, url).replace('%26', '&').lower()

            for source in scrape_source.getMore(url, hostDict):
                sources.append(source)

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---2EMBED Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
