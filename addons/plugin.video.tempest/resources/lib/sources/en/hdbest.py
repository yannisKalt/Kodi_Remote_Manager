# -*- coding: UTF-8 -*-
"""
    **Created by Tempest**
    **Thanks Jewbmx for the assist**
"""

import requests, re, json

from resources.lib.modules import cleantitle,directstream
from resources.lib.modules import source_utils, client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdbest.net']
        self.base_link = 'https://hdbest.net'
        self.movie_link = '?q=%s+%s'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0', 'Referer': self.base_link}
        self.session = requests.Session()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.geturl(title)
            url = self.base_link + self.movie_link % (mtitle.replace('-','+'), year)
            html = requests.get(url, headers=self.header).content
            match = re.compile('class="thumb".+?title="(.+?)".+?href="(.+?)">', re.DOTALL).findall(html)
            for item_url, url in match:
                check = '%s (%s)' % (title, year)
                if check not in item_url:
                    continue
                return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostprDict + hostDict
            r = requests.get(url).content
            link = client.parseDOM(r, 'iframe', ret='src')
            for url in link:
                if "api.hdv.fun" in url:
                    url = url.replace('https://api.hdv.fun/embed/', '')
                    apiurl = "https://api.hdv.fun/l1?imdb={}&ip=128.6.37.19".format(url)
                    movie_json = json.loads(self.session.post(apiurl).text)
                    url = movie_json[0]['src'][0]['src']
                    quainf = movie_json[0]['src'][0]['res']
                    quality, info = source_utils.get_release_quality(quainf, quainf)
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': True, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
