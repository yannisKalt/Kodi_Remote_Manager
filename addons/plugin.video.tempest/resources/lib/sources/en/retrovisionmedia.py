# -*- coding: utf-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse, traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.sources import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.retrovisionmedia.com']
        self.base_link = 'http://www.retrovisionmedia.com'
        self.search_link = '/?s=%s'
        self.headers={'User-Agent': client.agent(), 'Referer': self.base_link}

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

            hdlr = '%s %s' % (data['title'], int(data['year']))

            urls = self.search_link % urllib.quote_plus(data['title'])

            try:
                url = urlparse.urljoin(self.base_link, urls)
                posts = cfscrape.get(url, headers=self.headers).content
                r = [i for i in re.compile('href="(.+?)" title="(.+?)"').findall(posts) if hdlr in i[1]]
                r = [i for i in r]
                items += r
            except:
                return

            for item in items:
                try:
                    url = cfscrape.get(item[0], headers={'User-Agent': client.agent(), 'Referer': urls}).content
                    url = re.findall('src="(.+?)" type="video/mp4"', url)
                    for url in url:
                        sources.append(
                            {'source': 'CDN', 'quality': 'SD', 'language': 'en', 'url': url,
                             'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---RETROVISIONMEDIA Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
