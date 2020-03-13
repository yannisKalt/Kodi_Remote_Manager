# -*- coding: utf-8 -*-

"""
**Created by Tempest**

"""

import urllib, urlparse, requests
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import debrid, control
from resources.lib.modules import source_utils, rd_check

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.sceneddl.me']
        self.base_link = 'http://www.sceneddl.me'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status() is False: return
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if debrid.status() is False: return
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if debrid.status() is False: return
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

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (
                data['tvshowtitle'], int(data['season']), int(data['episode'])) \
                if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url).replace('-', '+')

            r = requests.get(url, headers=headers).content

            posts = client.parseDOM(r, "h2", attrs={"class": "entry-title"})
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
                    r = requests.get(i, headers=headers).content
                    u = client.parseDOM(r, "div", attrs={"class": "entry-content"})
                    for t in u:
                        r = client.parseDOM(t, 'a', ret='href')
                        for url in r:
                            if any(x in url for x in ['.rar']):
                                continue
                            quality, info = source_utils.get_release_quality(url)
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            info = ' | '.join(info)
                            if control.setting('deb.rd_check') == 'true':
                                check = rd_check.rd_deb_check(url)
                                if check:
                                    info = 'RD Checked' + ' | ' + info
                                    sources.append(
                                        {'source': host, 'quality': quality, 'language': 'en', 'url': check,
                                         'info': info, 'direct': False, 'debridonly': True})
                            else:
                                sources.append(
                                    {'source': host, 'quality': quality, 'language': 'en', 'url': url,
                                     'info': info, 'direct': False, 'debridonly': True})
                except:
                    pass
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Scenedll Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
