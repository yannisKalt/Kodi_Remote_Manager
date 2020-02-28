# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-24-2019 by JewBMX in Scrubs.
# Dupe of wsunblock. only real difference is search vs build.

import re, base64
from resources.lib.modules import cleantitle, source_utils
from resources.lib.sources import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['watchseriess.to']
        self.base_link = 'https://ww1.watchseriess.to'
        self.search_link = '/search/%s'
        self.show_link = '_s%s_e%s.html'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowTitle = cleantitle.geturl(tvshowtitle).replace(':', ' ').replace(' ', '+')
            url = self.base_link + self.search_link % tvshowTitle
            searchPage = cfscrape.get(url).content
            results = re.compile('<div valign="top" style="padding-left: 10px;">.+?<a href="(.+?)" title=".+?" target="_blank"><strong>(.+?)</strong></a>',re.DOTALL).findall(searchPage)
            for url, checkit in results:
                zcheck = '%s (%s)' % (tvshowtitle, year)
                if zcheck.lower() in checkit.lower():
                    url = url.replace('/serie/', '/episode/')
                    return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = self.base_link + url + self.show_link % (season, episode)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            r = cfscrape.get(url).content
            match = re.compile('cale\.html\?r=(.+?)" class="watchlink" title="(.+?)"').findall(r)
            for url, host in match:
                url = base64.b64decode(url)
                valid, host = source_utils.is_host_valid(host, hostDict)
                if valid:
                    quality, info = source_utils.get_release_quality(url, url)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False}) 
            return sources
        except Exception:
            return sources

    def resolve(self, url):
        return url
