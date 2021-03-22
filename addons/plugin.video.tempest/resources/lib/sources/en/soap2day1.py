# -*- coding: utf-8 -*-
# To Do: Add Tv
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse
import traceback
from resources.lib.modules import client
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.soap2day1.com']
        self.base_link = 'https://www.soap2day1.com'
        self.post_link = '/engine/ajax/search.php'

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

            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            post = 'do=search&subaction=search&story=%s' % urllib.quote_plus(query)

            try:
                r = client.request(self.base_link, post=post)
                r = client.parseDOM(r, 'div', attrs={'class': 'mov-i img-box'})
                r = [(re.findall('title="(.+?)" alt=".+?" />\n<div class=".+?" data-link="(.+?)"', i, re.DOTALL)) for i in r][0]
            except:
                return

            hostDict = hostprDict + hostDict

            for item in r:
                try:
                    name = item[0]
                    if data['title'] not in name:
                        continue

                    data = client.request(item[1])
                    url = re.findall('<iframe src="(.+?)" scrolling=".+?"', data, re.DOTALL)[0]
                    url = url.replace('https://myplayer.vip/', 'https://embed.mystream.to/')
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False,
                                        'debridonly': False})

                except:
                    pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---SOAP2DAY1 Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
