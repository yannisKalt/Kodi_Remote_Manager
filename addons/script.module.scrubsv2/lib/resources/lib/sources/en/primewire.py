# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.
# Made by SomeOne. Added .to domain and using it to prevent doom.

import re,urllib,urlparse
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import dom_parser2
from resources.lib.modules import jsunpack
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['primewire.ac', 'primewire.to']
        self.base_link = 'https://www.primewire.to/'
        self.moviesearch_link = '?keywords=%s&type=movie'
        self.tvsearch_link = '?keywords=%s&type=tv'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            query = self.moviesearch_link % urllib.quote_plus((title))
            query = urlparse.urljoin(self.base_link, query.lower())
            result = client.request(query, referer=self.base_link)
            result = client.parseDOM(result, 'div', attrs={'class': 'index_item.+?'})
            result = [(dom_parser2.parse_dom(i, 'a', req=['href', 'title'])[0]) for i in result if i]
            result = [(i.attrs['href']) for i in result if cleantitle.get(title) == cleantitle.get(re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '', i.attrs['title'], flags=re.I))][0]
            url = client.replaceHTMLCodes(result)
            url = url.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            query = self.tvsearch_link % urllib.quote_plus(cleantitle.query(tvshowtitle))
            query = urlparse.urljoin(self.base_link, query.lower())
            result = client.request(query)
            result = client.parseDOM(result, 'div', attrs={'class': 'index_item.+?'})
            result = [(dom_parser2.parse_dom(i, 'a', req=['href', 'title'])[0]) for i in result if i]
            result = [(i.attrs['href']) for i in result if cleantitle.get(tvshowtitle) == cleantitle.get(re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '', i.attrs['title'], flags=re.I))][0]
            url = client.replaceHTMLCodes(result)
            url = url.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = urlparse.urljoin(self.base_link, url) if url.startswith('/') else url
            url = url.split('online.html')[0]
            url = '%s%s-online.html' % (url, 'season-%01d-episode-%01d' % (int(season), int(episode)))
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources
            url = urlparse.urljoin(self.base_link, url) if not url.startswith('http') else url
            result = client.request(url)
            links = client.parseDOM(result, 'tbody')
            for i in links:
                try:
                    data = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'span', attrs={'class': 'version_host'})[0])][0]
                    url = urlparse.urljoin(self.base_link, data[0])
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')
                    host = data[1]
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if not valid:
                        raise Exception()
                    quality = client.parseDOM(i, 'span', ret='class')[0]
                    quality, info = source_utils.get_release_quality(quality, url)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
                except Exception:
                    pass
            return sources
        except Exception:
            return sources


    def resolve(self, url):
        try:
            if '/stream/' in url or '/watch/' in url:
                r = client.request(url, referer=self.base_link)
                link = client.parseDOM(r, 'a', ret='data-href', attrs={'id': 'iframe_play'})[0]
            else:
                try:
                    data = client.request(url, referer=self.base_link)
                    data = re.findall(r'\s*(eval.+?)\s*</script', data, re.DOTALL)[0]
                    link = jsunpack.unpack(data)
                    link = link.replace('\\', '')
                    link = re.findall(r'''go\(['"](.+?)['"]\)''', link)[0]
                except:
                    link = client.request(url, output='geturl', timeout=10)
                    if link == url:
                        return
                    else:
                        return link
            return link
        except:
            return

