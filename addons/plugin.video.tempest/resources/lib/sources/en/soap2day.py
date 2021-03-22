# -*- coding: utf-8 -*-

"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['soap2day.app']
        self.base_link = 'https://soap2day.app'
        self.post_link = '/engine/ajax/controller.php?mod=search'

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

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = data['title']
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            post = 'do=search&subaction=search&story=%s' % urllib.quote_plus(query)

            r = client.request(self.base_link, post=post)
            r = client.parseDOM(r, 'div', attrs={'class': 'thumbnail text-center'})
            for r in r:
                r = re.findall('<p><a href="(.+?)" title="(.+?)">.+?</a></p>', r, re.DOTALL)
                if data['title'] not in r[0][1]:
                    continue

            hostDict = hostprDict + hostDict

            for item in r:
                try:
                    data = client.request(item[0])
                    url = re.compile('src="(https://embed.mystream.+?)"').findall(data)
                    for url in url:
                        url = url.replace('https://embed.mystream.best/', 'https://embed.mystream.to/')
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            sources.append(
                                {'source': host, 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False,
                                 'debridonly': False})

                except:
                    pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---SOAP2DAY Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
