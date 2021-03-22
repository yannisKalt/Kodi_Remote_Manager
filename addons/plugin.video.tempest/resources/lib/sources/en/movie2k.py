# -*- coding: utf-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse, requests
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import scrape_source


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['movie2k.123movies.online']
        self.base_link = 'https://movie2k.123movies.online'
        self.search_link = '/?cat=tv&search=%s&exact=&actor=&director=&year=%s&advanced_search=true'
        self.search_link2 = '/?cat=movie&search=%s&exact=&actor=&director=&year=%s&advanced_search=true'
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
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            if 'tvshowtitle' in data:
                urls = self.search_link % (data['tvshowtitle'], data['year'])
                url = urlparse.urljoin(self.base_link, urls)
                posts = requests.get(url, headers={'User-Agent': client.agent(), 'Referer': urls}).content
                url = re.findall(
                    '<div class="title"><a title=".+?" href="(.+?)">(.+?)</a></div><div class="year"> (.+?)</div>',
                    posts)
                for url, title, year in url:
                    if data['tvshowtitle'] in title and data['year'] in year:
                        code = url.split('movie2k-')[1]
                        url = requests.get(url, headers={'User-Agent': client.agent(), 'Referer': urls}).content
                        url = "https://movie2k.123movies.online/watch-tv-%s-season-%s-episode-%s-online-movie2k-%s" % (data['tvshowtitle'], data['season'], data['episode'], code)
                        url = requests.get(url, headers={'User-Agent': client.agent(), 'Referer': url}).content
                        more_links = re.compile('<a href="(.+?)">View More Links</a></li></ul>').findall(url)[0]
                        if more_links:
                            url = requests.get(more_links,
                                               headers={'User-Agent': client.agent(), 'Referer': more_links}).content
                            url = re.findall('href="(.+?)" id="#iframe"', url)
                            items += url
                        else:
                            url = re.findall('href="(.+?)" id="#iframe"', url)
                            items += url

            else:
                urls = self.search_link2 % (data['title'], data['year'])
                url = urlparse.urljoin(self.base_link, urls)
                posts = requests.get(url, headers=self.headers).content
                url = re.findall(
                    '<div class="title"><a title=".+?" href="(.+?)">(.+?)</a></div><div class="year"> (.+?)</div>',
                    posts)
                for url, title, year in url:
                    if data['title'] in title and data['year'] in year:
                        url = self.base_link + url
                        url = requests.get(url, headers={'User-Agent': client.agent(), 'Referer': urls}).content
                        more_links = re.compile('<a href="(.+?)">View More Links</a></li></ul>').findall(url)[0]
                        url = re.compile('href="(.+?)" id="#iframe"').findall(url)
                        items += url

            for item in items:
                try:
                    url = requests.get(item, headers={'User-Agent': client.agent(), 'Referer': item}).content
                    url = re.findall('target="_blank">(.+?)</a>', url)[0]
                    if url.startswith('//'):
                        url = 'https:' + url
                    for source in scrape_source.getMore(url, hostDict):
                        sources.append(source)
                except:
                    pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---MOVIE2K Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        if 'jetload' in url:
            url = requests.get(url, headers=self.headers).content
            url = re.findall("var x_source = '(.+?)'", url)[0]
            return url
        else:
            return url
