# -*- coding: utf-8 -*-
"""
**Created by Tempest**

"""

import re,urllib,urlparse
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import debrid, control
from resources.lib.modules import source_utils, cache_check


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.link4file.com']
        self.base_link = 'http://www.link4file.com'
        self.search_link = '/download-search.php?q=%s&log=1&x=59&y=22'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources

            if debrid.status() is False:
                raise Exception()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url).replace('++', '+')

            r = client.request(url)

            posts = client.parseDOM(r, "div", attrs={"class": "content-fill"})
            hostDict = hostprDict + hostDict
            items = []
            for post in posts:
                try:
                    u = client.parseDOM(post, 'a', ret='href')
                    for i in u:
                        name = str(i)
                        items.append(name)
                except:
                    pass

            for item in items:
                try:
                    i = str(item)
                    i = urlparse.urljoin(self.base_link, i)
                    r = client.request(i)
                    u = client.parseDOM(r, "div", attrs={"class": "dl-links"})
                    for t in u:
                        url = re.compile('a href="javascript: dl(.+?)" rel=".+?"').findall(t)[0]
                        url = url.split("('")[1].split("')")[0]
                        quality, info = source_utils.get_release_quality(url, url)
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if control.setting('deb.cache_check') == 'true':
                            check = cache_check.rd_deb_check(url)
                            if not check:
                                continue
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                        else:
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                except:
                    pass
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Link4file Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
