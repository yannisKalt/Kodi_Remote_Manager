# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.
# Rewrote to be a little cleaner and get all the sources.

import re,base64
from resources.lib.modules import client
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['animepark.net']
        self.base_link = 'https://www.animepark.net'
        self.search_link = '/?s=%s'
        self.episode_link = '/%s-episode-%s'
        self.scraper = cfscrape.create_scraper()


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tv_maze = tvmaze.tvMaze()
            tvshowtitle = tv_maze.showLookup('thetvdb', tvdb)
            tvshowtitle = tvshowtitle['name']
            t = cleantitle.get(tvshowtitle)
            q = self.base_link + self.search_link %(tvshowtitle.replace(' ', '+'))
            r = self.scraper.get(q).content
            r = client.parseDOM(r, 'div', attrs={'class': 'anipost'})
            for i in r:
                match = re.compile('<a href="(.+?)".+?<span><b>Release Date:</b>(.+?)</span>',re.DOTALL).findall(i)
                for url, check in match:
                    if t in cleantitle.get(url):
                        if year in str(check):
                            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            tv_maze = tvmaze.tvMaze()
            num = tv_maze.episodeAbsoluteNumber(tvdb, int(season), int(episode))
            url = self.episode_link % (url.replace('https://www.animepark.net/', '').replace('/', ''), num)
            url = self.base_link + url
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict
            sources = []
            if url == None:
                return sources
            r = self.scraper.get(url).content
            match = re.compile('data-em="(.+?)"',re.DOTALL).findall(r)
            for iframe in match:
                html = base64.b64decode(iframe)
                try:
                    match = re.compile('<iframe src="(.+?)"').findall(html)
                except:
                    match = re.compile('<IFRAME SRC="(.+?)"').findall(html)
                for url in match:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(url, url)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
                    else:
                        if not url.startswith('http'):
                            url = self.base_link + url
                        r = self.scraper.get(url).content
                        try:
                            match = re.compile('<iframe src="(.+?)"').findall(r)
                        except:
                            match = re.compile('<source src="(.+?)"').findall(r)
                        for link in match:
                            valid, host = source_utils.is_host_valid(link, hostDict)
                            if valid:
                                quality, info = source_utils.get_release_quality(link, link)
                                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
                return url


