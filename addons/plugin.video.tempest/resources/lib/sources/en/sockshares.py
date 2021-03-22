# -*- coding: utf-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse, base64
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import scrape_source


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['sockshares.tv']
        self.base_link = 'https://sockshares.tv'
        self.search_link = '/search-movies/%s.html'
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
            items = []

            if url is None:
                return sources

            hostDict = hostprDict + hostDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = '%s: Season %s' % (title, data['season']) if 'tvshowtitle' in data else data['year']
            url = self.search_link % urllib.quote_plus(title)

            url = urlparse.urljoin(self.base_link, url)
            r = client.request(url, headers=self.headers)
            r = client.parseDOM(r, 'div', attrs={'class': 'thumb'})
            r = [re.findall('<a class="img" href="(.+?)".+?<b>(.+?)</b>.+?\s*.+?\b*\s*</a>\s*.+?<div class="status status-year">(.+?)</div>', i, re.DOTALL)[0] for i in r]
            items += r

            for item in items:
                try:
                    if 'tvshowtitle' in data:
                        if hdlr == item[1]:
                            url = client.request(item[0], headers=self.headers)
                            url = re.findall('href="(.+?)">(.+?)</a>', url)
                            for url in url:
                                if data['episode'] == url[1]:
                                    url = client.request(url[0], headers=self.headers)
                                    url = re.findall('<img src=".+?" width="16" height="16" /> <a href="(.+?)">Version ', url)
                                    i = 0
                                    for r in url:
                                        if i == 15:
                                            break
                                        r = client.request(r, headers=self.headers)
                                        r = re.compile('Base64\.decode\("(.+?)"').findall(r)
                                        for iframe in r:
                                            iframe = base64.b64decode(iframe)
                                            if '<img src' in iframe:
                                                r = re.compile('href="(.+?)"').findall(iframe)
                                                for url in r:
                                                    for source in scrape_source.getMore(url, hostDict):
                                                        sources.append(source)
                                                    i += 1
                                            else:
                                                r = re.compile('src="(.+?)"').findall(iframe)
                                                for url in r:
                                                    for source in scrape_source.getMore(url, hostDict):
                                                        sources.append(source)
                                                    i += 1
                    else:
                        if title == item[1] and data['year'] in item[2]:
                            url = client.request(item[0], headers=self.headers)
                            url = re.findall('<img src=".+?" width="16" height="16" /> <a href="(.+?)">Version ', url)
                            i = 0
                            for r in url:
                                if i == 20:
                                    break
                                r = client.request(r, headers=self.headers)
                                r = re.compile('Base64\.decode\("(.+?)"').findall(r)
                                for iframe in r:
                                    iframe = base64.b64decode(iframe)
                                    if '<img src' in iframe:
                                        r = re.compile('href="(.+?)"').findall(iframe)
                                        for url in r:
                                            for source in scrape_source.getMore(url, hostDict):
                                                sources.append(source)
                                            i += 1
                                    else:
                                        r = re.compile('src="(.+?)"').findall(iframe)
                                        for url in r:
                                            for source in scrape_source.getMore(url, hostDict):
                                                sources.append(source)
                                            i += 1
                except:
                    pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---2EMBED Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url

