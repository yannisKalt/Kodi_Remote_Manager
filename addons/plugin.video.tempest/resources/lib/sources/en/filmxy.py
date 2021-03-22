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
from resources.lib.modules import scrape_source


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.filmxy.tv']
        self.base_link = 'https://www.filmxy.tv'
        self.search_link = '/%s/'
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

            hostDict = hostprDict + hostDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = '%s-%s' % (data['title'].replace(' ', '-'), data['year'])
            query = re.sub('(\\\|/| -|:|\.|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % query
            url = urlparse.urljoin(self.base_link, url).lower()
            try:
                url = client.request(url, headers=self.headers)
                url = re.findall('data-player="&lt;iframe src=&quot;(.+?)&quot;', url)
                for url in url:
                    for source in scrape_source.getMore(url, hostDict):
                        sources.append(source)
            except:
                return

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---2EMBED Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
