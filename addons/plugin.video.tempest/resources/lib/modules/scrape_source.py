# -*- coding: utf-8 -*-

import re, json
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import control


# log_utils.log('---Testing - Exception: \n' + str(url))


def getMore(link, hostDict):
    sources = []
    if link is None:
        return sources
    if ' ' in link:
        link = link.replace(' ', '+')
    elif "gamovideo.com" in link:
        for source in gamovideo(link, hostDict):
            sources.append(source)
    elif "cloudvideo.tv" in link:
        for source in cloudvideo(link, hostDict):
            sources.append(source)
    elif "abcvideo.cc" in link:
        for source in abcvideo(link, hostDict):
            sources.append(source)
    elif "vidoza.net" in link:
        for source in vidoza(link, hostDict):
            sources.append(source)
    elif "upstream.to" in link:
        for source in upstream(link, hostDict):
            sources.append(source)
    elif "mixdrop.co" in link:
        for source in mixdrop(link, hostDict):
            sources.append(source)
    elif "mediashore.org" in link:
        for source in mediashore(link, hostDict):
            sources.append(source)
    elif "googleapis" in link:
        for source in sgoogle(link, hostDict):
            sources.append(source)
    elif "googleusercontent" in link:
        for source in sgoogle(link, hostDict):
            sources.append(source)
    elif "movcloud" in link:
        for source in movcloud(link, hostDict):
            sources.append(source)
    elif "vidcloud.pro" in link:
        for source in vidcloud_pro(link, hostDict):
            sources.append(source)
    elif 'vidcloud9' in link:
        for source in vidcloud9(link, hostDict):
            sources.append(source)
    elif 'vidsrc.me' in link:
        for source in vidsrc_me(link, hostDict):
            sources.append(source)
    elif '2embed' in link:
        for source in twoembed(link, hostDict):
            sources.append(source)
    elif 'vidnext.net' in link:
        for source in vidnext_net(link, hostDict):
            sources.append(source)
    elif 'vidoo' in link:
        for source in vidoo(link, hostDict):
            sources.append(source)
    elif 'hls3x.vidcloud9.com' in link:
        for source in hls3x(link, hostDict):
            sources.append(source)
    else:
        valid, host = source_utils.is_host_valid(link, hostDict)
        if valid:
            quality, info = source_utils.get_release_quality(link, link)
            if control.setting('dev') == 'true':
                log_utils.log('---SCRAPER Testing - Exception: \n' + str(link))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False,
                 'debridonly': False})
    return sources


def movcloud(link, hostDict):
    sources = []
    try:
        url = link.replace('https://movcloud.net/embed/', 'https://api.movcloud.net/stream/')
        url = client.request(url, headers={'User-Agent': client.agent(), 'Referer': 'https://movcloud.net'})
        url = json.loads(url)
        url = url['data']
        url = url['sources']
        for url in url:
            label = url['label']
            url = url['file']
            quality, info = source_utils.get_release_quality(label, label)
            if control.setting('dev') == 'true':
                log_utils.log('---MOVCLOUD Testing - Exception: \n' + str(url))
            sources.append(
                {'source': 'movcloud', 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False,
                 'debridonly': False})
        return sources
    except:
        return []
    return []


def vidcloud9(link, hostDict):
    sources = []
    try:
        url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
        url = re.compile('data-video="(.+?)">.+?</li>').findall(url)
        for url in url:
            if url.startswith('//'):
                url = 'https:' + url
            if 'vidnext.net' in url:
                if '&typesub' in url:
                    url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
                    url = re.findall("file: '(.+?)'", url)[0]
                    if control.setting('dev') == 'true':
                        log_utils.log('---VIDCLOUD9_VIDNEXT_HLS Testing - Exception: \n' + str(url))
                    sources.append(
                        {'source': 'HLS', 'quality': 'SD', 'language': 'en', 'url': url,
                         'direct': False, 'debridonly': False})
                else:
                    url = client.request(url, headers={'User-Agent': client.agent(), 'Referer': link})
                    url = re.findall('data-video="(.+?)">', url)
                    for url in url:
                        if url.startswith('//'):
                            url = 'https:' + url
                        if 'vidnext.net' in url:
                            url = client.request(url, headers={'User-Agent': client.agent(), 'Referer': url})
                            r = re.findall('(ep.+?.m3u8)', url)
                            for r in r:
                                url = url.split('ep')[0]
                                url = url + r
                                if '.720.m3u8' in url:
                                    quality = '720p'
                                else:
                                    quality = 'SD'
                                if control.setting('dev') == 'true':
                                    log_utils.log('---VIDCLOUD9_VIDNEXT_HLS3X Testing - Exception: \n' + str(url))
                                sources.append(
                                    {'source': 'HLS3X', 'quality': quality, 'language': 'en', 'url': url,
                                     'direct': False, 'debridonly': False})
                        else:
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            if valid:
                                if control.setting('dev') == 'true':
                                    log_utils.log('---VIDCLOUD9_VIDNEXT Testing - Exception: \n' + str(url))
                                quality, info = source_utils.get_release_quality(url, url)

                                sources.append(
                                    {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url,
                                     'direct': False, 'debridonly': False})

            elif 'movcloud' in url:
                url = url.replace('https://movcloud.net/embed/', 'https://api.movcloud.net/stream/')
                url = client.request(url, headers={'User-Agent': client.agent(), 'Referer': 'https://movcloud.net'})
                url = json.loads(url)
                url = url['data']
                url = url['sources']
                for url in url:
                    label = url['label']
                    url = url['file']
                    if control.setting('dev') == 'true':
                        log_utils.log('---MOVCLOUD Testing - Exception: \n' + str(url))
                    quality, info = source_utils.get_release_quality(label, label)
                    sources.append(
                        {'source': 'movcloud', 'quality': quality, 'language': 'en', 'info': info, 'url': url,
                         'direct': False, 'debridonly': False})
            else:
                valid, host = source_utils.is_host_valid(url, hostDict)
                if control.setting('dev') == 'true':
                    log_utils.log('---VIDCLOUD9_1 Testing - Exception: \n' + str(url))
                if valid:
                    quality, info = source_utils.get_release_quality(url, url)
                    sources.append(
                        {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url,
                         'direct': False, 'debridonly': False})
        return sources
    except:
        return []
    return []


def vidcloud_pro(link, hostDict):
    sources = []
    try:
        url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
        url = re.findall('sources = \[{"file":"(.+?)","type"', url)[0]
        url = url.replace('\\', '')
        valid, host = source_utils.is_host_valid(link, hostDict)
        if valid:
            if control.setting('dev') == 'true':
                log_utils.log('---VIDCLOUD_PRO Testing - Exception: \n' + str(url))
            quality, info = source_utils.get_release_quality(url, url)
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url,
                 'direct': False, 'debridonly': False})
        return sources
    except:
        return []
    return []


def vidsrc_me(link, hostDict):
    sources = []
    try:
        r = client.request(link, headers={'User-Agent': client.agent(), 'Referer': 'https://v2.vidsrc.me'})
        r = re.findall('data-hash="(.+?)"', r)[0]
        r = 'https://v2.vidsrc.me/src/%s' % r
        url = client.request(r, headers={'User-Agent': client.agent(), 'Referer': 'https://v2.vidsrc.me'})
        url = re.findall("'player' src='(.+?)'", url)[0]
        url = url + '|Referer=https://vidsrc.me'
        if control.setting('dev') == 'true':
            log_utils.log('---VIDSRC_ME Testing - Exception: \n' + str(url))
        quality, info = source_utils.get_release_quality(url, url)
        sources.append(
            {'source': 'CDN', 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': True,
             'debridonly': False})
        return sources
    except:
        return []
    return []


def twoembed(link, hostDict):
    sources = []
    items = []
    try:
        r = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
        r = re.compile('data-id="(.+?)">.+?</a>').findall(r)
        r = [i for i in r]
        items += r

        for item in items:
            item = 'https://www.2embed.ru/ajax/embed/play?id=%s&_token=' % item
            url = client.request(item, headers={'User-Agent': client.agent(), 'Referer': item})
            url = re.findall('"link":"(.+?)","sources"', url)
            for url in url:
                if 'vidcloud.pro' in url:
                    r = client.request(url, headers={'User-Agent': client.agent(), 'Referer': url})
                    r = re.findall('sources = \[{"file":"(.+?)","type"', r)[0]
                    r = r.replace('\\', '')
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    quality, info = source_utils.get_release_quality(url, url)
                    sources.append(
                        {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': r,
                         'direct': False, 'debridonly': False})
                else:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        if control.setting('dev') == 'true':
                            log_utils.log('---TWOEMBED Testing - Exception: \n' + str(url))
                        quality, info = source_utils.get_release_quality(url, url)
                        sources.append(
                            {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url,
                             'direct': False,
                             'debridonly': False})
        return sources
    except:
        return []
    return []


def vidnext_net(link, hostDict):
    sources = []
    try:
        if 'vidnext.net' in link:
            if '&typesub' in link:
                url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
                url = re.findall("file: '(.+?)'", url)[0]
                if control.setting('dev') == 'true':
                    log_utils.log('---VIDNEXT_HLS Testing - Exception: \n' + str(url))
                sources.append(
                    {'source': 'HLS', 'quality': 'SD', 'language': 'en', 'url': url,
                     'direct': False, 'debridonly': False})
            else:
                url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
                url = re.findall('data-video="(.+?)">', url)
                for url in url:
                    if url.startswith('//'):
                        url = 'https:' + url
                    if 'vidnext.net' in url:
                        url = client.request(url, headers={'User-Agent': client.agent(), 'Referer': url})
                        r = re.findall('(ep.+?.m3u8)', url)
                        for r in r:
                            url = url.split('ep')[0]
                            url = url + r
                            if '.720.m3u8' in url:
                                quality = '720p'
                            else:
                                quality = 'SD'
                            if control.setting('dev') == 'true':
                                log_utils.log('---VIDNEXT_HLS3X Testing - Exception: \n' + str(url))
                            sources.append(
                                {'source': 'HLS3X', 'quality': quality, 'language': 'en', 'url': url, 'direct': False,
                                 'debridonly': False})

        else:
            valid, host = source_utils.is_host_valid(link, hostDict)
            if valid:
                if control.setting('dev') == 'true':
                    log_utils.log('---VIDNEXT_1 Testing - Exception: \n' + str(link))
                quality, info = source_utils.get_release_quality(link, link)
                sources.append(
                    {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False,
                     'debridonly': False})

        return sources
    except:
        return []
    return []


def hls3x(link, hostDict):
    sources = []
    try:
        url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
        r = re.findall('(ep.+?.m3u8)', url)
        for r in r:
            url = url.split('ep')[0]
            url = url + r
            if '.720.m3u8' in url:
                quality = '720p'
            else:
                quality = 'SD'
            info = source_utils.get_release_quality(url)
            if control.setting('dev') == 'true':
                log_utils.log('---HLS3X Testing - Exception: \n' + str(url))
            sources.append(
                {'source': 'HLS3X', 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False,
                 'debridonly': False})
        return sources
    except:
        return []
    return []


def vidoo(link, hostDict):
    sources = []
    try:
        url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
        r = re.findall('file:"(.+?)"\},\{file:".+?",label:"(.+?)"', url)
        for r in r:
            quality, info = source_utils.get_release_quality(r[1], r[0])
            r = client.request(r[0], headers={'User-Agent': client.agent(), 'Referer': link})
            r = re.findall('(https://.+?m3u8)', r)[0]
            if control.setting('dev') == 'true':
                log_utils.log('---VIDOO Testing - Exception: \n' + str(r))
            sources.append(
                {'source': 'VIDOO', 'quality': quality, 'language': 'en', 'info': info, 'url': r, 'direct': False,
                 'debridonly': False})
        return sources
    except:
        return []
    return []


def mediashore(link, hostDict):
    sources = []
    try:
        try:
            url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
            r = re.findall('<title>(.+?)</title>', url)[0]
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(r, r)
            if control.setting('dev') == 'true':
                log_utils.log('---MEDIASHORE Testing - Exception: \n' + str(r))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': r, 'direct': False,
                 'debridonly': False})
        except:
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(link, link)
            if control.setting('dev') == 'true':
                log_utils.log('---MEDIASHORE Testing - Exception: \n' + str(link))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False,
                 'debridonly': False})
        return sources
    except:
        return []
    return []


def abcvideo(link, hostDict):
    sources = []
    try:
        try:
            if 'html' in link:
                url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
                r = re.findall('jwplayer.qualityLabel\', \'(.+?)\'', url)[0]
                valid, host = source_utils.is_host_valid(link, hostDict)
                quality, info = source_utils.get_release_quality(r, r)
                if control.setting('dev') == 'true':
                    log_utils.log('---ABCVIDEO Testing - Exception: \n' + str(r))
                sources.append(
                    {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': r, 'direct': False,
                     'debridonly': False})
            else:
                url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
                r = re.findall('<title>(.+?)</title>', url)[0]
                valid, host = source_utils.is_host_valid(link, hostDict)
                quality, info = source_utils.get_release_quality(r, r)
                if control.setting('dev') == 'true':
                    log_utils.log('---ABCVIDEO Testing - Exception: \n' + str(r))
                sources.append(
                    {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': r, 'direct': False,
                     'debridonly': False})
        except:
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(link, link)
            if control.setting('dev') == 'true':
                log_utils.log('---ABCVIDEO Testing - Exception: \n' + str(link))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False,
                 'debridonly': False})
        return sources
    except:
        return []
    return []


def cloudvideo(link, hostDict):
    sources = []
    try:
        try:
            url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
            r = re.findall('<title>(.+?)</title>', url)[0]
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(r, r)
            if control.setting('dev') == 'true':
                log_utils.log('---CLOUDVIDEO Testing - Exception: \n' + str(r))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': r, 'direct': False,
                 'debridonly': False})
        except:
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(link, link)
            if control.setting('dev') == 'true':
                log_utils.log('---CLOUDVIDEO Testing - Exception: \n' + str(link))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False,
                 'debridonly': False})
        return sources
    except:
        return []
    return []


def gamovideo(link, hostDict):
    sources = []
    try:
        try:
            url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
            r = re.findall('<Title>(.+?)</Title>', url)[0]
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(r, r)
            if control.setting('dev') == 'true':
                log_utils.log('---GAMOVIDEO Testing - Exception: \n' + str(r))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': r, 'direct': False,
                 'debridonly': False})
        except:
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(link, link)
            if control.setting('dev') == 'true':
                log_utils.log('---GAMOVIDEO Testing - Exception: \n' + str(link))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False,
                 'debridonly': False})
        return sources
    except:
        return []
    return []


def mixdrop(link, hostDict):
    sources = []
    try:
        try:
            url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
            r = re.findall('target="_blank">(.+?)</a>', url)[0]
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(r, r)
            if control.setting('dev') == 'true':
                log_utils.log('---MIXDROP Testing - Exception: \n' + str(r))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': r, 'direct': False,
                 'debridonly': False})
        except:
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(link, link)
            if control.setting('dev') == 'true':
                log_utils.log('---MIXDROP Testing - Exception: \n' + str(link))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False,
                 'debridonly': False})
        return sources
    except:
        return []
    return []


def upstream(link, hostDict):
    sources = []
    try:
        try:
            url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
            r = re.findall('</i>(.+?)</span>', url)[0]
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(r, r)
            if control.setting('dev') == 'true':
                log_utils.log('---UPSTREAM Testing - Exception: \n' + str(r))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': r, 'direct': False,
                 'debridonly': False})
        except:
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(link, link)
            if control.setting('dev') == 'true':
                log_utils.log('---UPSTREAM Testing - Exception: \n' + str(link))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False,
                 'debridonly': False})
        return sources
    except:
        return []
    return []


def vidoza(link, hostDict):
    sources = []
    try:
        try:
            url = client.request(link, headers={'User-Agent': client.agent(), 'Referer': link})
            r = re.findall('CONTENT="(.+?)">', url)[0]
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(r, r)
            if control.setting('dev') == 'true':
                log_utils.log('---VIDOZA Testing - Exception: \n' + str(r))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': r, 'direct': False,
                 'debridonly': False})
        except:
            valid, host = source_utils.is_host_valid(link, hostDict)
            quality, info = source_utils.get_release_quality(link, link)
            if control.setting('dev') == 'true':
                log_utils.log('---VIDOZA Testing - Exception: \n' + str(link))
            sources.append(
                {'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False,
                 'debridonly': False})
        return sources
    except:
        return []
    return []


def sgoogle(link, hostDict):
    sources = []
    try:
        if control.setting('dev') == 'true':
            log_utils.log('---GOOGLE_1 Testing - Exception: \n' + str(link))
        sources.append({'source': 'gvideo', 'quality': 'SD', 'language': 'en', 'url': link,
                        'direct': True, 'debridonly': False})
        return sources
    except:
        return []
    return []
