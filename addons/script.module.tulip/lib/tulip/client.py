# -*- coding: utf-8 -*-

'''
    Tulip routine libraries, based on lambda's lamlib
    Author Twilight0

        License summary below, for more details please read license.txt file

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 2 of the License, or
        (at your option) any later version.
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import absolute_import, division, print_function

from tulip.cleantitle import replaceHTMLCodes
from tulip.parsers import parseDOM
from tulip.user_agents import randomagent, random_mobile_agent
import re, sys, time, traceback, gzip, json, socket
from os import sep
from os.path import basename, splitext
from tulip import cache, control
from tulip.log import log_debug
from kodi_six.xbmc import log

from tulip.compat import (
    urllib2, cookielib, urlparse, URLopener, quote_plus, unquote, str,
    urlsplit, urlencode, bytes, is_py3, addinfourl, py3_dec, iteritems, StringIO
)

PROGRESS = control.enum(OFF=0, WINDOW=1, BACKGROUND=2)


# noinspection PyUnboundLocalVariable
def request(
        url, close=True, redirect=True, error=False, proxy=None, post=None, headers=None, mobile=False, limit=None,
        referer=None, cookie=None, output='', timeout='30', username=None, password=None, verify=True, as_bytes=False
):

    try:
        url = url.decode('utf-8')
    except Exception:
        pass

    if isinstance(post, dict):
        post = bytes(urlencode(post), encoding='utf-8')
    elif isinstance(post, str) and is_py3:
        post = bytes(post, encoding='utf-8')

    try:
        handlers = []

        if username is not None and password is not None and not proxy:

            passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passmgr.add_password(None, uri=url, user=username, passwd=password)
            handlers += [urllib2.HTTPBasicAuthHandler(passmgr)]
            opener = urllib2.build_opener(*handlers)
            urllib2.install_opener(opener)

        if proxy is not None:

            if username is not None and password is not None:
                passmgr = urllib2.ProxyBasicAuthHandler()
                passmgr.add_password(None, uri=url, user=username, passwd=password)
                handlers += [
                    urllib2.ProxyHandler({'http': '{0}'.format(proxy)}), urllib2.HTTPHandler,
                    urllib2.ProxyBasicAuthHandler(passmgr)
                ]
            else:
                handlers += [urllib2.ProxyHandler({'http':'{0}'.format(proxy)}), urllib2.HTTPHandler]
            opener = urllib2.build_opener(*handlers)
            urllib2.install_opener(opener)

        if output == 'cookie' or output == 'extended' or close is not True:

            cookies = cookielib.LWPCookieJar()
            handlers += [urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(cookies)]

            opener = urllib2.build_opener(*handlers)
            urllib2.install_opener(opener)

        try:
            import platform
            is_XBOX = platform.uname()[1] == 'XboxOne'
        except Exception:
            is_XBOX = False

        if not verify and sys.version_info >= (2, 7, 12):

            try:

                import ssl
                ssl_context = ssl._create_unverified_context()
                handlers += [urllib2.HTTPSHandler(context=ssl_context)]
                opener = urllib2.build_opener(*handlers)
                urllib2.install_opener(opener)

            except Exception:

                pass

        elif verify and ((2, 7, 8) < sys.version_info < (2, 7, 12) or is_XBOX):

            try:

                import ssl
                try:
                    import _ssl
                    CERT_NONE = _ssl.CERT_NONE
                except Exception:
                    CERT_NONE = ssl.CERT_NONE
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = CERT_NONE
                handlers += [urllib2.HTTPSHandler(context=ssl_context)]
                opener = urllib2.build_opener(*handlers)
                urllib2.install_opener(opener)

            except Exception:

                pass

        try:
            headers.update(headers)
        except Exception:
            headers = {}

        if 'User-Agent' in headers:
            pass
        elif mobile is not True:
            #headers['User-Agent'] = agent()
            headers['User-Agent'] = cache.get(randomagent, 12)
        else:
            headers['User-Agent'] = cache.get(random_mobile_agent, 12)

        if 'Referer' in headers:
            pass
        elif referer is None:
            headers['Referer'] = '%s://%s/' % (urlparse(url).scheme, urlparse(url).netloc)
        else:
            headers['Referer'] = referer

        if not 'Accept-Language' in headers:
            headers['Accept-Language'] = 'en-US'

        if 'Cookie' in headers:
            pass
        elif cookie is not None:
            headers['Cookie'] = cookie

        if redirect is False:

            class NoRedirectHandler(urllib2.HTTPRedirectHandler):

                def http_error_302(self, reqst, fp, code, msg, head):

                    infourl = addinfourl(fp, head, reqst.get_full_url())
                    infourl.status = code
                    infourl.code = code

                    return infourl

                http_error_300 = http_error_302
                http_error_301 = http_error_302
                http_error_303 = http_error_302
                http_error_307 = http_error_302

            opener = urllib2.build_opener(NoRedirectHandler())
            urllib2.install_opener(opener)

            try:
                del headers['Referer']
            except Exception:
                pass

        req = urllib2.Request(url, data=post, headers=headers)

        try:

            response = urllib2.urlopen(req, timeout=int(timeout))

        except urllib2.HTTPError as response:

            if response.code == 503:

                if 'cf-browser-verification' in response.read(5242880):

                    netloc = '{0}://{1}'.format(urlparse(url).scheme, urlparse(url).netloc)

                    cf = cache.get(Cfcookie.get, 168, netloc, headers['User-Agent'], timeout)

                    headers['Cookie'] = cf

                    req = urllib2.Request(url, data=post, headers=headers)

                    response = urllib2.urlopen(req, timeout=int(timeout))

                elif error is False:
                    return

            elif error is False:
                return

        if output == 'cookie':

            try:
                result = '; '.join(['%s=%s' % (i.name, i.value) for i in cookies])
            except Exception:
                pass

            try:
                result = cf
            except Exception:
                pass

        elif output == 'response':

            if limit == '0':
                result = (str(response.code), response.read(224 * 1024))
            elif limit is not None:
                result = (str(response.code), response.read(int(limit) * 1024))
            else:
                result = (str(response.code), response.read(5242880))

        elif output == 'chunk':

            try:
                content = int(response.headers['Content-Length'])
            except Exception:
                content = (2049 * 1024)

            if content < (2048 * 1024):
                return
            result = response.read(16 * 1024)

        elif output == 'extended':

            try:
                cookie = '; '.join(['%s=%s' % (i.name, i.value) for i in cookies])
            except Exception:
                pass

            try:
                cookie = cf
            except Exception:
                pass

            content = response.headers
            result = response.read(5242880)

            if not as_bytes:

                result = py3_dec(result)

            return result, headers, content, cookie

        elif output == 'geturl':

            result = response.geturl()

        elif output == 'headers':

            content = response.headers

            if close:
                response.close()

            return content

        elif output == 'file_size':

            try:
                content = int(response.headers['Content-Length'])
            except Exception:
                content = '0'

            response.close()

            return content

        elif output == 'json':

            content = json.loads(response.read(5242880))

            response.close()

            return content

        else:

            if limit == '0':
                result = response.read(224 * 1024)
            elif limit is not None:
                if isinstance(limit, int):
                    result = response.read(limit * 1024)
                else:
                    result = response.read(int(limit) * 1024)
            else:
                result = response.read(5242880)

        if close is True:
            response.close()

        if not as_bytes:
            result = py3_dec(result)

        return result

    except Exception as reason:

        _, __, tb = sys.exc_info()

        print(traceback.print_tb(tb))
        log('Client module failed, reason of failure: ' + repr(reason))

        return


def retriever(source, destination, user_agent=None, referer=None, reporthook=None, data=None, **kwargs):

    if user_agent is None:
        user_agent = cache.get(randomagent, 12)

    if referer is None:
        referer = '{0}://{1}/'.format(urlparse(source).scheme, urlparse(source).netloc)

    class Opener(URLopener):

        version = user_agent

        def __init__(self):

            URLopener.__init__(self)

            headers = [('User-Agent', self.version), ('Accept', '*/*'), ('Referer', referer)]

            if kwargs:
                headers.extend(iteritems(kwargs))

            self.addheaders = headers

    Opener().retrieve(source, destination, reporthook, data)


def url2name(url):

    url = url.split('|')[0]
    return basename(unquote(urlsplit(url)[2]))


def get_extension(url, response):

    filename = url2name(url)
    if 'Content-Disposition' in response.info():
        cd_list = response.info()['Content-Disposition'].split('filename=')
        if len(cd_list) > 1:
            filename = cd_list[-1]
            if filename[0] == '"' or filename[0] == "'":
                filename = filename[1:-1]
    elif response.url != url:
        filename = url2name(response.url)
    ext = splitext(filename)[1][1:]
    if not ext:
        ext = 'mp4'
    return ext


# noinspection PyUnresolvedReferences
def download_media(url, path, file_name, initiate_int='', completion_int='', exception_int='', progress=None):

    try:
        if progress is None:
            progress = int(control.setting('progress_dialog'))

        active = not progress == PROGRESS.OFF
        background = progress == PROGRESS.BACKGROUND

        if isinstance(initiate_int, int):
            line1 = control.lang(initiate_int).format(file_name)
        else:
            line1 = 'Downloading {0}'.format(file_name)

        with control.ProgressDialog(control.addonInfo('name'), line1, background=background, active=active) as pd:

            try:
                headers = dict([item.split('=') for item in (url.split('|')[1]).split('&')])
                for key in headers:
                    headers[key] = unquote(headers[key])
            except:
                headers = {}

            if 'User-Agent' not in headers:
                headers['User-Agent'] = cache.get(randomagent, 12)

            request = urllib2.Request(url.split('|')[0], headers=headers)
            response = urllib2.urlopen(request)

            if 'Content-Length' in response.info():
                content_length = int(response.info()['Content-Length'])
            else:
                content_length = 0

            file_name += '.' + get_extension(url, response)
            full_path = control.join(path, file_name)
            log_debug('Downloading: %s -> %s' % (url, full_path))

            path = control.transPath(control.legalfilename(path))

            try:
                control.makeFiles(path)
            except Exception as e:
                log_debug('Path Create Failed: %s (%s)' % (e, path))

            if not path.endswith(sep):
                path += sep
            if not control.exists(path):
                raise Exception('Failed to create dir')

            file_desc = control.openFile(full_path, 'w')
            total_len = 0
            cancel = False
            while 1:
                data = response.read(512 * 1024)
                if not data:
                    break

                if pd.is_canceled():
                    cancel = True
                    break

                total_len += len(data)
                if not file_desc.write(data):
                    raise Exception('Failed to write file')

                percent_progress = total_len * 100 / content_length if content_length > 0 else 0
                log_debug('Position : {0} / {1} = {2}%'.format(total_len, content_length, percent_progress))
                pd.update(percent_progress)

            file_desc.close()

        if not cancel:

            if isinstance(completion_int, int):
                control.infoDialog(control.lang(completion_int).format(file_name))
            else:
                control.infoDialog('Download_complete for file name {0}'.format(file_name))

            log_debug('Download Complete: {0} -> {1}'.format(url, full_path))

    except Exception as e:

        log_debug('Error ({0}) during download: {1} -> {2}'.format(str(e), url, file_name))
        if isinstance(exception_int, int):
            control.infoDialog(control.lang(exception_int).format(str(e), file_name))
        else:
            control.infoDialog('Download_complete for file name {0}'.format(file_name))


def parse_headers(string):

    """
    Converts a multi-line response/request headers string into a dictionary
    :param string: string of headers
    :return: dictionary of response headers
    """

    headers = dict([line.partition(': ')[::2] for line in string.splitlines()])

    return headers


def stripTags(html):

    sub_start = html.find("<")
    sub_end = html.find(">")
    while sub_end > sub_start > -1:
        html = html.replace(html[sub_start:sub_end + 1], "").strip()
        sub_start = html.find("<")
        sub_end = html.find(">")

    return html


class Cfcookie:

    def __init__(self):
        self.cookie = None

    def get(self, netloc, ua, timeout):

        try:

            self.netloc = netloc
            self.ua = ua
            self.timeout = timeout
            self.cookie = None
            self._get_cookie(netloc, ua, timeout)

            if self.cookie is None:
                log_debug('%s returned an error. Could not collect tokens.' % netloc)

            return self.cookie

        except Exception as e:

            log_debug('%s returned an error. Could not collect tokens - Error: %s.' % (netloc, str(e)))

            return self.cookie

    def _get_cookie(self, netloc, ua, timeout):

        class NoRedirection(urllib2.HTTPErrorProcessor):

            def http_response(self, request, response):

                return response

        def parseJSString(s):

            try:

                offset = 1 if s[0] == '+' else 0
                val = int(
                    eval(s.replace('!+[]', '1').replace('!![]', '1').replace('[]', '0').replace('(', 'str(')[offset:]))
                return val

            except:

                pass

        cookies = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cookies))
        opener.addheaders = [('User-Agent', ua)]

        try:

            response = opener.open(netloc, timeout=int(timeout))
            result = response.read()

        except urllib2.HTTPError as response:

            result = response.read()

            try:
                encoding = response.info().getheader('Content-Encoding')
            except Exception:
                encoding = None

            if encoding == 'gzip':
                result = gzip.GzipFile(fileobj=StringIO(result)).read()

        jschl = re.compile('name="jschl_vc" value="(.+?)"/>').findall(result)[0]
        init = re.compile(r'setTimeout\(function\(\){\s*.*?.*:(.*?)};').findall(result)[0]
        builder = re.compile(r"challenge-form\'\);\s*(.*)a.v").findall(result)[0]

        if '/' in init:
            init = init.split('/')
            decryptVal = parseJSString(init[0]) / float(parseJSString(init[1]))
        else:
            decryptVal = parseJSString(init)

        lines = builder.split(';')
        for line in lines:
            if len(line) > 0 and '=' in line:
                sections = line.split('=')
                if '/' in sections[1]:
                    subsecs = sections[1].split('/')
                    line_val = parseJSString(subsecs[0]) / float(parseJSString(subsecs[1]))
                else:
                    line_val = parseJSString(sections[1])
                decryptVal = float(eval('%.16f' % decryptVal + sections[0][-1] + '%.16f' % line_val))

        answer = float('%.10f' % decryptVal) + len(urlparse(netloc).netloc)

        query = '%scdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s' % (netloc, jschl, answer)

        if 'type="hidden" name="pass"' in result:
            passval = re.findall('name="pass" value="(.*?)"', result)[0]
            query = '%scdn-cgi/l/chk_jschl?pass=%s&jschl_vc=%s&jschl_answer=%s' % (
                netloc, quote_plus(passval), jschl, answer)
            time.sleep(6)

        opener.addheaders = [('User-Agent', ua),
                             ('Referer', netloc),
                             ('Accept', 'text/html, application/xhtml+xml, application/xml, */*'),
                             ('Accept-Encoding', 'gzip, deflate')]

        response = opener.open(query)
        response.close()

        cookie = '; '.join(['%s=%s' % (i.name, i.value) for i in cookies])

        if 'cf_clearance' in cookie:
            self.cookie = cookie


def parseJSString(s):
    try:
        offset = 1 if s[0] == '+' else 0
        val = int(eval(s.replace('!+[]', '1').replace('!![]', '1').replace('[]','0').replace('(', 'str(')[offset:]))
        return val
    except Exception:
        pass


def check_connection(host="1.1.1.1", port=53, timeout=3):

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


__all__ = [
    'parseDOM', 'request', 'stripTags', 'retriever', 'replaceHTMLCodes', 'parseJSString', 'parse_headers',
    'url2name', 'get_extension', 'check_connection'
]
