# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 06-20-2019 by JewBMX in Scrubs.

import re,base64
from resources.lib.modules import cleantitle,source_utils,cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['sharemovies.net']
        self.base_link = 'http://sharemovies.net'
        self.search_link = '/search-movies/%s.html'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            q = cleantitle.geturl(title) + '+' + year
            q2 = q.replace('-','+')
            url = self.base_link + self.search_link % q2
            r = self.scraper.get(url).content
            match = re.compile('<div class="title"><a href="(.+?)">(.+?)</a></div>').findall(r)
            for url, check in match:
                tity = '%s (%s)' % (title, year)
                if tity not in check:
                    raise Exception()
                return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return sources
            q = url + '-season-' + season
            q2 = url.replace('-','+')
            url = self.base_link + self.search_link % q2
            r = self.scraper.get(url).content
            match = re.compile('<div class="title"><a href="(.+?)-' + q + '\.html"').findall(r)
            for url in match:
                url = '%s-%s.html' % (url, q)
                r = self.scraper.get(url).content
                match = re.compile('<a class="episode episode_series_link" href="(.+?)">' + episode + '</a>').findall(r)
                for url in match:
                    return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            if url == None:
                return sources
            sources = []
            r = self.scraper.get(url).content
            try:
                match = re.compile('themes/movies/img/icon/server/(.+?)\.png" width="16" height="16" /> <a href="(.+?)">Version ').findall(r)
                for host, url in match:
                    if host == 'internet':
                        pass
                    if source_utils.limit_hosts() is True and host in str(sources):
                        continue
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            except:
                return
        except Exception:
            return
        return sources


    def resolve(self, url):
        r = self.scraper.get(url).content
        match = re.compile('Base64\.decode\("(.+?)"').findall(r)
        for iframe in match:
            iframe = base64.b64decode(iframe)
            match = re.compile('src="(.+?)"').findall(iframe)
            for url in match:
                return url

