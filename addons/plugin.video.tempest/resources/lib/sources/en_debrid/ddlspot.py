# -*- coding: utf-8 -*-
"""
**Created by Tempest**

"""

import re,urllib,urlparse
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import control
from resources.lib.modules import source_utils
from resources.lib.modules import rd_check


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.ddlspot.com']
        self.base_link = 'http://www.ddlspot.com/'
        self.search_link = 'search/?q=%s&m=1&x=0&y=0'

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

            r = client.request(url)

            posts = client.parseDOM(r, "table", attrs={"class": "download"})
            hostDict = hostprDict + hostDict
            items = []
            for post in posts:
                try:
                    u = client.parseDOM(post, 'a', ret='href')
                    for i in u:
                        try:
                            name = str(i)
                            items.append(name)
                        except:
                            pass
                except:
                    pass

            for item in items:
                try:
                    info = []

                    i = str(item)
                    i = self.base_link + i
                    r = client.request(i)
                    u = client.parseDOM(r, "div", attrs={"class": "dl-links"})
                    for t in u:
                        r = re.compile('a href=".+?" rel=".+?">(.+?)<').findall(t)
                        for url in r:
                            if any(x in url for x in ['.rar', '.zip', '.iso']):
                                raise Exception()
                            quality, info = source_utils.get_release_quality(url)
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            if control.setting('deb.rd_check') == 'true':
                                check = rd_check.rd_deb_check(url)
                                if check:
                                    info = 'RD Checked' + '|' + info
                                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                            else:
                                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})

                except:
                    pass
            check = [i for i in sources if not i['quality'] == 'CAM']
            if check: sources = check

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Ddlspot Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
