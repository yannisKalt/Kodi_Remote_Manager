# -*- coding: utf-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse, base64
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['dbgo.fun']
        self.base_link = 'https://dbgo.fun'
        self.search_link = '/video.php?id=%s'
        self.headers = {'Referer': 'https://cdn.dbgo.fun'}

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

            if url is None:
                return sources

            hostDict = hostprDict + hostDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            url = self.search_link % urllib.quote_plus(data['imdb'])
            url = urlparse.urljoin(self.base_link, url)
            try:
                url = client.request(url, headers=self.headers)
                url = re.findall('file:"#2(.*?)"', url)[0].replace('//eS95L3kv', '').replace('//ei96L3ov', '').replace('//eC94L3gv', '')
                url = base64.b64decode(url) + '|Referer=https://cdn.dbgo.fun/'
                sources.append({'source': 'CDN', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            except:
                pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---DBGO Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
