# -*- coding: utf-8 -*-
# Need to work on Tvshows a little more
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
        self.domains = ['vidnext.net']
        self.base_link = 'https://vidnext.net'
        self.search_link = '/search.html?keyword=%s'
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
            hdlr = '%s - Season %s' % (data['tvshowtitle'], data['season']) if 'tvshowtitle' in data else data['year']

            query = '%s season %s' % (
                data['tvshowtitle'], data['season']) if 'tvshowtitle' in data else '%s' % (
                data['title'])
            query = re.sub('(\\\|/| -|:|\.|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % query
            url = urlparse.urljoin(self.base_link, url).replace(' ', '+').lower()

            r = client.request(url, headers=self.headers)
            r = client.parseDOM(r, 'li', attrs={'class': 'video-block '})
            r = [re.findall(
                '<a href="(.+?)">\s*\b*\s*\b*\s*.+?\s*</div>\s*\b*\s*\b*\s*<div class="name">\s*(.+?)\s*<\b*\s*.+?\s*<span class="date">(.+?)-.+?</span>',
                i, re.DOTALL)[0] for i in r]

            for item in r:
                if 'tvshowtitle' in data:
                    if data['title'] in item[1]:
                        t = urlparse.urljoin(self.base_link, item[0])
                        t = client.request(t, headers=self.headers)
                        t = re.findall('<iframe src="(.+?)"', t)[0]
                        if t.startswith('//'):
                            t = 'https:' + t
                        t = client.request(t, headers={'User-Agent': client.agent(), 'Referer': t})
                        t = re.compile('data-video="(.+?)">.+?</li>').findall(t)
                        t = [i for i in t]
                        items += t
                    else:
                        if hdlr in item[1]:
                            t = urlparse.urljoin(self.base_link, item[0])
                            r = client.request(t, headers=self.headers)
                            t = client.parseDOM(r, 'li', attrs={'class': 'video-block '})
                            t = re.findall(
                                '<a href="(.+?)">.+?<div class="img">.+?<div class="picture">\s*<img onerror="this.src=\'.+?\';" src=".+?" alt="(.+?)" />',
                                r, re.DOTALL)
                            for r in t:
                                if data['title'] in r[1]:
                                    t = urlparse.urljoin(self.base_link, r[0])
                                    t = client.request(t, headers=self.headers)
                                    t = re.findall('<iframe src="(.+?)"', t)[0]
                                    if t.startswith('//'):
                                        t = 'https:' + t
                                    t = client.request(t, headers={'User-Agent': client.agent(), 'Referer': t})
                                    t = re.compile('data-video="(.+?)">.+?</li>').findall(t)
                                    t = [i for i in t]
                                    items += t


                else:
                    if data['title'] in item[1] and hdlr in item[2]:
                        t = urlparse.urljoin(self.base_link, item[0])
                        t = client.request(t, headers=self.headers)
                        t = re.findall('<iframe src="(.+?)"', t)[0]
                        if t.startswith('//'):
                            t = 'https:' + t
                        t = client.request(t, headers={'User-Agent': client.agent(), 'Referer': t})
                        t = re.compile('data-video="(.+?)">.+?</li>').findall(t)
                        t = [i for i in t]
                        items += t

            for url in items:
                if url.startswith('//'):
                    url = 'https:' + url
                for source in scrape_source.getMore(url, hostDict):
                    sources.append(source)

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---VIDNEXT Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
