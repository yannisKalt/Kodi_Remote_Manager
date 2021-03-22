# -*- coding: utf-8 -*-
# Add tvshows later(only a few on site)
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['allmoviesforyou.co']
        self.base_link = 'https://allmoviesforyou.co'
        self.search_link = '/?s=%s'
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

            query = '%s S%02dE%02d' % (
            data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s' % (
            data['title'])
            query = re.sub('(\\\|/| -|:|\.|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url).lower()

            r = client.request(url, headers=self.headers)

            r = client.parseDOM(r, 'article', attrs={'class': 'TPost B'})
            r = [re.findall(
                '<a href="(.+?)">.+?<span class="Qlty">(.+?)</span>.+?<span class="Qlty Yr">(.+?)</span>.+?<h2 class="Title">(.+?)</h2>',
                i, re.DOTALL)[0] for i in r]
            items += r

            for item in items:
                try:
                    if data['title'] in item[3] and data['year'] in item[2]:
                        url = client.request(item[0], headers=self.headers)
                        url = re.findall('<iframe src="(.+?)"', url)[0]
                        url = url.replace('#038;', '')
                        url = client.request(url, headers=self.headers)
                        url = re.findall('src="(.+?)"', url)

                        for url in url:
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            sources.append(
                                {'source': host, 'quality': item[1], 'language': 'en', 'url': url,
                                 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---ALLMOVIESFORYOU Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
