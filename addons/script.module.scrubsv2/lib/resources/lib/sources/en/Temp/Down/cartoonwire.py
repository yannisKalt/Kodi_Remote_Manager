# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 05-06-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import client,cleantitle
from resources.lib.modules import directstream,source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['watchcartoononline.info', 'cartoonwire.to']
        self.base_link = 'https://watchcartoononline.info'
        self.search_link = '/?s=%s'
        # https://watchcartoononline.info/?s=zeroman


    # https://watchcartoononline.info/wonder-park-2019/
    # https://watchcartoononline.info/friends-naki-on-the-monster-island-2011/
    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = '%s-%s' % (title, year)
            url = self.base_link + '/' + url
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            headers = {'User-Agent': client.randomagent()}
            tvtit = cleantitle.geturl(tvshowtitle)
            url = self.base_link + self.search_link % tvtit
            r = client.request(url, headers=headers, timeout='3')
            u = client.parseDOM(r, "div", attrs={"class": "ml-item"})
            for i in u:
                t = re.compile('<a href="(.+?)"').findall(i)
                for r in t:
                    if cleantitle.get(tvtit) in cleantitle.get(r):
                        return source_utils.strip_domain(url)
        except:
            return


    # https://watchcartoononline.info/episode/zeroman-episode-13/
    # https://watchcartoononline.info/episode/guardians-of-the-galaxy-season-3-episode-23/
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            if season == '1': 
                url = self.base_link + '/episode/' + url + '-episode-' + episode
            else:
                url = self.base_link + '/episode/' + url + '-season-' + season + '-episode-' + episode
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        headers = {'User-Agent': client.randomagent()}
        if url == None: return sources
        try:
            r = client.request(url, headers=headers, timeout='3')
            try:
                match = re.compile('var filmId = "(.+?)"').findall(r)
                for film_id in match:
                    server = 'vip'
                    url = self.base_link + '/ajax-get-link-stream/?server=' + server + '&filmId=' + film_id
                    r = client.request(url, headers=headers, timeout='3')
                    if r == '':
                        pass
                    else:
                        quality = source_utils.check_url(r)
                        r = client.request(r, headers=headers, timeout='3')
                        match = re.compile('<iframe src="(.+?)"').findall(r)
                        for url in match:
                            sources.append({ 'source': server, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False })
                    server = 'streamango'
                    url = self.base_link + '/ajax-get-link-stream/?server=' + server + '&filmId=' + film_id
                    r = client.request(url, headers=headers, timeout='3')
                    if r == '':
                        pass
                    else:
                        quality = source_utils.check_url(r)
                        r = client.request(r, headers=headers, timeout='3')
                        match = re.compile('<iframe src="(.+?)"').findall(r)
                        for url in match:
                            sources.append({ 'source': server, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False })
                    server = 'openload'
                    url = self.base_link + '/ajax-get-link-stream/?server=' + server + '&filmId=' + film_id
                    r = client.request(url)
                    if r == '':
                        pass
                    else:
                        quality = source_utils.check_url(r)
                        r = client.request(r, headers=headers, timeout='3')
                        match = re.compile('<iframe src="(.+?)"').findall(r)
                        for url in match:
                            sources.append({ 'source': server, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False })
                    server = 'rapidvideo'
                    url = self.base_link + '/ajax-get-link-stream/?server=' + server + '&filmId=' + film_id
                    r = client.request(url)
                    if r == '':
                        pass
                    else:
                        quality = source_utils.check_url(r)
                        r = client.request(r, headers=headers, timeout='3')
                        match = re.compile('<iframe src="(.+?)"').findall(r)
                        for url in match:
                            sources.append({ 'source': server, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False })
                    server = 'photo'
                    url = self.base_link + '/ajax-get-link-stream/?server=' + server + '&filmId=' + film_id
                    r = client.request(url, headers=headers, timeout='3')
                    if r == '':
                        pass
                    else:
                        quality = source_utils.check_url(r)
                        sources.append({ 'source': 'GDrive', 'quality': quality, 'language': 'en', 'url': r, 'direct': False, 'debridonly': False })
            except:
                return
        except Exception:
            return
        return sources


    def resolve(self, url):
        return url


