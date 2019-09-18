# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 04-15-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import source_utils,cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['deepmovie.ch']
        self.base_link = 'https://www.deepmovie.ch/%s/'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link % imdb
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None: return sources
            r = self.scraper.get(url).content
            try:
                match = re.compile('<iframe.+?src="(.+?)"').findall(r)
                for url in match:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if 'youtube' in host: continue
                    if valid:
                        sources.append({ 'source': host, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False })
            except:
                return
        except:
            return
        return sources


    def resolve(self, url):
        return url

