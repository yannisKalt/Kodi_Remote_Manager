# -*- coding: utf-8 -*-
"""
**Created by Tempest**

"""

import urllib, urlparse
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client, control
from resources.lib.modules import debrid, cache_check
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['onceddl.net']
        self.base_link = 'https://onceddl.net'
        self.search_link = '/?s=%s'

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
            if url is None:
                return

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

            if url is None:
                return sources

            if debrid.status() is False:
                raise Exception()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (
                data['tvshowtitle'], int(data['season']), int(data['episode'])) \
                if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url).replace('-', '+').replace('%3A+', '+')

            r = client.request(url)

            posts = client.parseDOM(r, "div", attrs={"class": "inner-center"})
            hostDict = hostprDict + hostDict
            items = []
            for post in posts:
                try:
                    u = client.parseDOM(post, 'a', ret='href')
                    for i in u:
                        name = str(i)
                        items.append(name)
                except:
                    pass

            for item in items:
                try:
                    i = str(item)
                    r = client.request(i)
                    u = client.parseDOM(r, "div", attrs={"class": "single-link"})
                    for t in u:
                        r = client.parseDOM(t, 'a', ret='href')
                        for url in r:
                            if 'www.share-online.biz' in url:
                                continue
                            quality, info = source_utils.get_release_quality(url)
                            if 'SD' in quality:
                                continue
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            if control.setting('deb.cache_check') == 'true':
                                check = cache_check.rd_deb_check(url)
                                if not check:
                                    continue
                                sources.append(
                                    {'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                     'direct': False, 'debridonly': True})
                            else:
                                sources.append(
                                    {'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                     'direct': False, 'debridonly': True})
                except:
                    pass
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Onceddl Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
