# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 03-17-2019 by JewBMX in Scrubs.
# -Fixed by Tempest

import re,urllib,urlparse,json,time
import traceback
from resources.lib.modules import client,debrid,source_utils,control
from resources.lib.modules import log_utils
from resources.lib.modules import cache_check, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.tvsearch = 'https://torrentapi.org/pubapi_v2.php?app_id=Torapi&token={0}&mode=search&search_string={1}&{2}'
        self.msearch = 'https://torrentapi.org/pubapi_v2.php?app_id=Torapi&token={0}&mode=search&search_imdb={1}&{2}'
        self.token = 'https://torrentapi.org/pubapi_v2.php?app_id=Torapi&get_token=get_token'

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
            if url is None:
                return sources
            if debrid.status() is False:
                raise Exception()
            if debrid.torrent_enabled() is False:
                raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s' % data['imdb']
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            token = client.getHTML(self.token)
            token = json.loads(token)["token"]
            if 'tvshowtitle' in data:
                search_link = self.tvsearch.format(token, urllib.quote_plus(query), 'format=json_extended')
            else:
                search_link = self.msearch.format(token, data['imdb'], 'format=json_extended')
            time.sleep(2)
            rjson = client.getHTML(search_link)
            files = json.loads(rjson)['torrent_results']
            for file in files:
                name = file["title"]
                quality, info = source_utils.get_release_quality(name, name)
                size = source_utils.convert_size(file["size"])
                info.append(size)
                info = ' | '.join(info)
                url = file["download"]
                url = url.split('&tr')[0]
                if control.setting('torrent.cache_check') == 'true':
                    cached = cache_check.rd_cache_check(url)
                    if not cached:
                        continue
                    sources.append({'source': 'Cached Torrent', 'quality': quality, 'language': 'en', 'url': url,
                                    'info': info, 'direct': False, 'debridonly': True})
                else:
                    sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                    'direct': False, 'debridonly': True})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Torrapi Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
