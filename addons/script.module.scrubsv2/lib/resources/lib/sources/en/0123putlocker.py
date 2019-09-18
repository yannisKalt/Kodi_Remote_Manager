# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.

import re,base64
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['putlockertv.ws']
        self.base_link = 'http://putlockertv.ws'
        self.search_link = '/search-movies/%s.html'
        self.scraper = cfscrape.create_scraper()
        # Old 0123putlocker.com  Now craptcha


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            url = url.replace('-','+')
            return url
        except:
            return
 
 
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            query = url + '+season+' + season
            find = query.replace('+','-')
            url = self.base_link + self.search_link % query
            r = self.scraper.get(url).content
            match = re.compile('<a href="http://putlockertv.ws/watch/(.+?)-' + find + '.html"').findall(r)
            for url_id in match:
                url = 'http://putlockertv.ws/watch/' + url_id + '-' + find + '.html'
                r = self.scraper.get(url).content
                match = re.compile('<a class="episode episode_series_link" href="(.+?)">' + episode + '</a>').findall(r)
                for url in match:
                    return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = self.scraper.get(url).content
            match = re.compile('<p class="server_version"><img src="http://putlockertv.ws/themes/movies/img/icon/server/(.+?).png" width="16" height="16" /> <a href="(.+?)">').findall(r)
            for host, url in match:
                if host == 'internet':
                    pass
                if source_utils.limit_hosts() is True and host in str(sources):
                    continue
                valid, host = source_utils.is_host_valid(host, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False}) 
            return sources
        except Exception:
            return sources


    def resolve(self, url):
        r = self.scraper.get(url).content
        match = re.compile('decode\("(.+?)"').findall(r)
        for info in match:
            info = base64.b64decode(info)
            match = re.compile('src="(.+?)"').findall(info)
            for url in match:
                return url


