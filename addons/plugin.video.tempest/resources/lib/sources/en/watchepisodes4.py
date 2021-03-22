# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 01-09-2021 by Tempest.

import re
import traceback
from resources.lib.modules import client
from resources.lib.modules import log_utils
from resources.lib.modules import cleantitle
from resources.lib.modules import scrape_source


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['watchepisodes4.com']
        self.base_link = 'https://www.watchepisodes4.com/'
        self.headers = {'User-Agent': client.agent()}

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(tvshowtitle)
            url = self.base_link + clean_title
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            r = client.request(url, headers=self.headers)

            r = re.compile('<a title=".+? Season ' + season + ' Episode ' + episode + ' .+?" href="(.+?)">').findall(r)
            for url in r:
                return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict
            r = client.request(url, headers=self.headers)
            r = re.compile('class="watch-button" data-actuallink="(.+?)"').findall(r)
            for url in r:
                for source in scrape_source.getMore(url, hostDict):
                    sources.append(source)
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---WATCHEPSODES4 Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
