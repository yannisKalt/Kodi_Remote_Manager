# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 04-14-2020 by Tempest.

import urllib, urlparse, re
import traceback
from resources.lib.modules import client
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_source
from resources.lib.sources import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']  # Old  tinklepad.is  movie25.hk
        self.domains = ['5movies.to']
        self.base_link = 'https://5movies.to'
        self.search_link = '/search.php?q=%s'
        self.video_link = '/getlink.php?Action=get&lk=%s'
        self.headers = {'User-Agent': client.agent()}

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

    def _search(self, title, year, headers):
        try:
            if 'It Chapter Two' in title:
                title = 'It: Chapter Two'
            else:
                title
            if 'Philosopher\'s' in title:
                title = title.replace('Philosopher\'s', 'Sorcerer\'s')
            else:
                title
            q = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(title))
            r = cfscrape.get(q, headers=self.headers).content
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-img'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            url = [i for i in r if title in i[1] and year in i[1]][0][0]
            return url
        except:
            pass

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources

            hostDict = hostprDict + hostDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            headers = {}
            if 'tvshowtitle' in data:
                episode = data['episode']
                season = data['season']
                url = self._search(data['tvshowtitle'], data['year'], headers)
                url = url.replace('online-free', 'season-%s-episode-%s-online-free' % (season, episode))
            else:
                url = self._search(data['title'], data['year'], headers)
            url = url if 'http' in url else urlparse.urljoin(self.base_link, url)
            result = cfscrape.get(url, headers=self.headers).content
            result = client.parseDOM(result, 'li', attrs={'class': 'link-button'})
            links = client.parseDOM(result, 'a', ret='href')
            i = 0
            for t in links:
                if i == 25:
                    break
                try:
                    t = t.split('=')[1]
                    t = urlparse.urljoin(self.base_link, self.video_link % t)
                    result = client.request(t, post={}, headers={'User-Agent': client.agent(), 'Referer': url})
                    if 'href=' in result:
                        result = re.findall("href='(.+?)'", result)[0]
                    u = result if 'http' in result else 'http:' + result
                    u = u.replace('http:', 'https:')
                    u.decode('utf-8')
                    for source in scrape_source.getMore(u, hostDict):
                        sources.append(source)
                    i += 1
                except:
                    pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---5MOVIES Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
