# -*- coding: utf-8 -*-
# -Cleaned and Checked on 02-26-2019 by JewBMX in Scrubs.
#Created by Tempest

import re, urllib, urlparse
from resources.lib.modules import client,debrid,source_utils,cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['best-moviez.ws']
        self.base_link = 'https://www.best-moviez.ws/'
        self.search_link = '?s=%s&submit=Search'
        self.scraper = cfscrape.create_scraper()


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
            if url == None: return

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
            if url == None: return sources
            if debrid.status() is False: raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s S%02dE%02d' % (
                data['tvshowtitle'], int(data['season']), int(data['episode'])) \
                if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)
            headers = {'Referer': url}
            r = self.scraper.get(url, headers=headers).content
            for loopCount in range(0, 2):
                if loopCount == 1 or (r == None and 'tvshowtitle' in data):
                    headers = {'Referer':  url}
                    r = self.scraper.get(url, headers=headers).content
                    posts = client.parseDOM(r, "div", attrs={"id": "content"})
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
                    if len(items) > 0: break
            for item in items:
                try:
                    hdlr = hdlr.lower()
                    if not hdlr in item: continue
                    i = str(item)
                    headers = {'Referer': url}
                    r = self.scraper.get(i, headers=headers).content
                    u = client.parseDOM(r, "div", attrs={"class": "entry-content"})
                    for t in u:
                        r = client.parseDOM(t, 'a', ret='href')
                        for url in r:
                            if 'zippyshare' in url: continue
                            quality, info = source_utils.get_release_quality(url)
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                except:
                    pass
            return sources
        except:
            return sources


    def resolve(self, url):
        return url

