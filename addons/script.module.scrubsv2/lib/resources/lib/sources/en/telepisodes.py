# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2018 by JewBMX in Scrubs.

from resources.lib.modules import cleantitle
from resources.lib.modules import getSum
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['telepisodes.org']
        self.base_link = 'https://www.telepisodes.org'
        self.tvshow_link = '/tv-series/%s/season-%s/episode-%s/'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            tvshowtitle = url
            url = self.base_link + self.tvshow_link % (tvshowtitle, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            hostDict = hostprDict + hostDict
            page = getSum.get(url)
            match = getSum.findEm(page, '<a class="linkdomx w3-button w3-blue w3-center" rel="nofollow" title="(.+?)" target="_blank" href="(.+?)"')
            if match:
                for hoster, url in match:
                    url = self.base_link + url
                    valid, host = source_utils.is_host_valid(hoster, hostDict)
                    if valid:
                        if source_utils.limit_hosts() is True and host in str(sources):
                            continue
                        sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            page2 = getSum.get(url)
            match2 = getSum.findEm(page2, 'class="mybutton vidlink button-link" target="_blank" href="/open/site/(.+?)"')
            if match2:
                for link in match2:
                    link = self.base_link + "/open/site/" + link
                    url = getSum.get(link, Type='redirect')
                    return url
        except:
            return


