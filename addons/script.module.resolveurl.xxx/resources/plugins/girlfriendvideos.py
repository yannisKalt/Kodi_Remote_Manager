'''
    resolveurl XBMC Addon
    Copyright (C) 2016 Gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import re, urlparse
from resolveurl import common
from resolveurl.plugins.lib import helpers
from resolveurl.resolver import ResolveUrl, ResolverError

class GirlfriendVideosResolver(ResolveUrl):
    name = 'girlfriendvideos'
    domains = ['girlfriendvideos.com']
    pattern = '(?://|\.)(girlfriendvideos\.com)/(members/[a-z]{1}/\w+/\d+.php)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA}
        html = self.net.http_GET(web_url, headers=headers).content
            
        if html:
            try:
                headers.update({'Referer': web_url})
                html = html.replace('\\','')
                pattern = r"""<video src="([^"]+)"""
                link = re.search(pattern,html)
                return urlparse.urljoin('http://www.girlfriendvideos.com', link.groups()[0])  + helpers.append_headers(headers)
            except:
                raise ResolverError('File not found')
                
        raise ResolverError('File not found')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='http://{host}/{media_id}')

    @classmethod
    def _is_enabled(cls):
        return True
