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
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.lunchflix.net', 'www.lunchflix.com']
        self.base_link = 'https://www.lunchflix.net'
        self.search_link = '/?s=%s'
        self.headers = {'User-Agent': client.agent(), 'Referer': self.base_link}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
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

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            hdlr = '%s (%s)' % (data['title'].replace("Philosopher's", "Sorcerer&#8217;s"), int(data['year']))
            query = '%s %s' % (data['title'], int(data['year']))

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url).replace('Philosopher', 'Sorcerer')
            try:
                posts = requests.get(url, headers=self.headers).content
                r = [i for i in re.findall('title="(.+?)" href="(.+?)"', posts) if hdlr in i[0]]
                items += r
            except:
                pass

            for item in items:
                r = requests.get(item[1], headers=self.headers).content
                url = re.findall('playlist: "(.+?)"', r)[0]
                url = requests.get(url, headers=self.headers).content
                url = re.findall('"file":"(.+?)",', url)[0]
                quality, info = source_utils.get_release_quality(url)
                sources.append(
                    {'source': 'CDN', 'quality': quality, 'language': 'en', 'url': url,
                     'info': info, 'direct': True, 'debridonly': False})

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---LUNCHFLIX Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
