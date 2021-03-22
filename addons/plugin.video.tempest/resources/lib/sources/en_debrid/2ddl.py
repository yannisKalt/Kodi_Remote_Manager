# -*- coding: utf-8 -*-

"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse, traceback

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import source_utils
from resources.lib.modules import log_utils
from resources.lib.modules import rd_check
from resources.lib.modules import control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['2ddl.ms', 'onceddl.org', 'onceddl.net']
        self.base_link = 'https://2ddl.ms'
        self.search_link = '/?q=%s'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status() is False: return
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if debrid.status() is False: return
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if debrid.status() is False: return
        try:
            if url is None: return

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

            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (
            data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
            data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|\.|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url).replace('%3A+', '-').replace('+', '-').replace('--', '-').lower()

            r = client.request(url, headers=self.headers)
            r = client.parseDOM(r, 'h2', attrs={'class': 'title'})
            r = [re.findall('<a class=""\s*href="(.+?)"\s*title="(.+?)"', i, re.DOTALL)[0] for i in r]

            hostDict = hostprDict + hostDict

            items = []

            for item in r:
                try:
                    t = item[1]
                    t1 = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '', t)

                    if not cleantitle.get(t1) == cleantitle.get(title): raise Exception()

                    y = re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*|S\d*)[\.|\)|\]|\s]', t)[-1].upper()

                    if not y == hdlr: raise Exception()

                    data = client.request(item[0], headers=self.headers)
                    data = re.compile('<a href="(.+?)" target="_blank">.+?<').findall(data)
                    u = [(t, i) for i in data]
                    items += u
                except:
                    pass

            for item in items:
                try:
                    name = item[0]
                    name = client.replaceHTMLCodes(name)

                    quality, info = source_utils.get_release_quality(name, item[1])

                    url = item[1]
                    if any(x in url for x in ['.rar', '.zip', '.iso', 'www.share-online.biz', 'https://ouo.io',
                                              'http://guard.link']): raise Exception()
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    valid, host = source_utils.is_host_valid(url, hostDict)
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    info = ' | '.join(info)
                    if control.setting('deb.rd_check') == 'true':
                        check = rd_check.rd_deb_check(url)
                        if check:
                            info = 'RD Checked' + ' | ' + info
                            sources.append(
                                {'source': host, 'quality': quality, 'language': 'en', 'url': check, 'info': info,
                                 'direct': False, 'debridonly': True})
                    else:
                        sources.append(
                            {'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                             'direct': False, 'debridonly': True})
                except:
                    pass

            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('---ONCEDDL Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
