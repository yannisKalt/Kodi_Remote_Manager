# -*- coding: utf-8 -*-


import traceback
import re
import urllib2
import json
from resources.lib.modules import control, log_utils


def rd_cache_check(url):
    from resolveurl.plugins.realdebrid import RealDebridResolver
    from resolveurl import common
    net = common.Net()
    #USER_AGENT = 'ResolveURL for Kodi/%s' % control.getKodiVersion()
    token = RealDebridResolver.get_setting('token')
    headers = {'Authorization': 'Bearer %s' % token}
    rest_base_url = 'https://api.real-debrid.com/rest/1.0'
    check_cache_path = 'torrents/instantAvailability'
    try:
        if url.lower().startswith('magnet:'):
            r = re.search('''magnet:.+?urn:([a-zA-Z0-9]+):([a-zA-Z0-9]+)''', url.lower(), re.I)
            if r:
                _hash, _format = r.group(2).lower(), r.group(1)
                try:
                    url = '%s/%s/%s' % (rest_base_url, check_cache_path, _hash)
                    result = net.http_GET(url, headers=headers).content
                    js_result = json.loads(result)
                    _hash_info = js_result.get(_hash, {})
                    if isinstance(_hash_info, dict):
                        if len(_hash_info.get('rd')) > 0:
                            if control.setting('addon_debug') == 'true':
                                log_utils.log('Real-Debrid: %s is readily available to stream' % _hash)
                                log_utils.log('Real-Debrid: %s ' % _hash_info)
                            return _hash_info
                except urllib2.HTTPError as e:
                    log_utils.log("Real-Debrid Error: CHECK CACHE | %s" % e)
                    if e.code == 401:
                        try:
                            RealDebridResolver().refresh_token()
                            url = '%s/%s/%s' % (rest_base_url, check_cache_path, _hash)
                            result = net.http_GET(url, headers=headers).content
                            js_result = json.loads(result)
                            _hash_info = js_result.get(_hash, {})
                            if isinstance(_hash_info, dict):
                                if len(_hash_info.get('rd')) > 0:
                                    if control.setting('addon_debug') == 'true':
                                        log_utils.log('Real-Debrid: %s is readily available to stream' % _hash)
                                        log_utils.log('Real-Debrid: %s ' % _hash_info)
                                    return _hash_info
                        except Exception as e:
                            log_utils.log("Real-Debrid Error: CHECK CACHE | %s" % e)
                            raise
                    else:
                        return
        else:
            return
    except Exception:
        failure = traceback.format_exc()
        log_utils.log('Debrid - Check Torrent Cache - Exception: ' + str(failure))
        return {}


def rd_deb_check(url):
    from resolveurl.plugins.realdebrid import RealDebridResolver
    from resolveurl import common
    net = common.Net()
    #USER_AGENT = 'ResolveURL for Kodi/%s' % control.getKodiVersion()
    token = RealDebridResolver.get_setting('token')
    headers = {'Authorization': 'Bearer %s' % token}
    rest_base_url = 'https://api.real-debrid.com/rest/1.0'
    unrestrict_link_path = 'unrestrict/link'
    try:
        if url.lower():
            try:
                urls = '%s/%s' % (rest_base_url, unrestrict_link_path)
                data = {'link': url}
                result = net.http_POST(urls, form_data=data, headers=headers).content
                js_result = json.loads(result)
                if "streamable" in js_result:
                    if js_result['streamable'] == 1:
                        return True
            except urllib2.HTTPError as e:
                log_utils.log("Real-Debrid Error: CHECK CACHE | %s" % e)
                if e.code == 401:
                    try:
                        RealDebridResolver().refresh_token()
                        urls = '%s/%s' % (rest_base_url, unrestrict_link_path)
                        data = {'link': url}
                        result = net.http_POST(urls, form_data=data, headers=headers).content
                        js_result = json.loads(result)
                        if 'streamable' in js_result:
                            if js_result['streamable'] == 1:
                                return True
                    except Exception as e:
                        log_utils.log("Real-Debrid Error: CHECK SOURCE | %s" % e)
                        raise
                else:
                    return
        else:
            return
    except Exception:
        failure = traceback.format_exc()
        log_utils.log('Debrid - Check Deb - Exception: ' + str(failure))
        return False
