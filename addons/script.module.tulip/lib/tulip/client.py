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

from __future__ import absolute_import, division

from tulip.user_agents import randomagent, random_mobile_agent
import re, sys, time
from tulip import cache, control
from tulip.log import log_debug
from kodi_six.xbmc import log

from tulip.compat import (
    urllib2, cookielib, urlparse, URLopener, quote_plus, unquote, unicode, unescape, range, basestring, str,
    urlsplit, urlencode, bytes, is_py3, addinfourl
)


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
    elif isinstance(post, basestring) and is_py3:
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

                    cf = cache.get(cfcookie, 168, netloc, headers['User-Agent'], timeout)

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

            if is_py3 and not as_bytes and isinstance(result, bytes):
                result = result.decode('utf-8')

            return result, headers, content, cookie

        elif output == 'geturl':
            result = response.geturl()

        elif output == 'headers':

            content = response.headers

            return content

        else:
            if limit == '0':
                result = response.read(224 * 1024)
            elif limit is not None:
                result = response.read(int(limit) * 1024)
            else:
                result = response.read(5242880)

        if close is True:
            response.close()

        if is_py3 and not as_bytes and isinstance(result, bytes):
            result = result.decode('utf-8')

        return result

    except Exception as reason:
        log('Client module failed, reason of failure: ' + repr(reason))
        return


def retriever(source, destination, user_agent=None, referer=None, *args):

    if user_agent is None:
        user_agent = cache.get(randomagent, 12)

    class Opener(URLopener):
        version = user_agent

        def __init__(self):
            URLopener.__init__(self)
            self.addheaders = [('User-Agent', self.version), ('Accept', '*/*'), ('Referer', referer)]

    Opener().retrieve(source, destination, *args)


def url2name(url):

    from os.path import basename

    url = url.split('|')[0]
    return basename(unquote(urlsplit(url)[2]))


def get_extension(url, response):

    from os.path import splitext

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


def enum(**enums):

    return type(b'Enum', (), enums)


def download_media(url, path, file_name, initiate_int='', completion_int='', exception_int='', progress=None):

    PROGRESS = enum(OFF=0, WINDOW=1, BACKGROUND=2)

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

            from os import sep

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


def parseDOM(html, name=u"", attrs=None, ret=False):

    """
    :param html:
        String to parse, or list of strings to parse.
    :type html:
        string or list
    :param name:
        Element to match ( for instance "span" )
    :type name:
        string
    :param attrs:
        Dictionary with attributes you want matched in the elment (for
        instance { "id": "span3", "class": "oneclass.*anotherclass",
        "attribute": "a random tag" } )
    :type attrs:
        dict
    :param ret:
        Attribute in element to return value of. If not set(or False), returns
        content of DOM element.
    :type ret:
        string
    """

    if attrs is None:
        attrs = {}

    # log_debug("Name: " + repr(name) + " - Attrs:" + repr(attrs) + " - Ret: " + repr(ret) + " - HTML: " + str(type(html)))

    if isinstance(name, basestring):  # Should be handled

        try:
            name = name.decode("utf-8")
        except Exception:
            pass
            # log_debug("Couldn't decode name binary string: " + repr(name))

    if isinstance(html, basestring):
        try:
            html = [html.decode("utf-8")]  # Replace with chardet thingy
        except Exception:
            html = [html]
    elif isinstance(html, unicode):
        html = [html]
    elif not isinstance(html, list):
        log_debug("Input isn't list or string/unicode.")
        return u""

    if not name.strip():
        log_debug("Missing tag name")
        return u""

    ret_lst = []
    for item in html:
        temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
        for match in temp_item:
            item = item.replace(match, match.replace("\n", " "))

        lst = _getDOMElements(item, name, attrs)

        if isinstance(ret, basestring):
            # log_debug("Getting attribute %s content for %s matches " % (ret, len(lst) ))
            lst2 = []
            for match in lst:
                lst2 += _getDOMAttributes(match, name, ret)
            lst = lst2
        else:
            # log_debug("Getting element content for %s matches " % len(lst))
            lst2 = []
            for match in lst:
                # log_debug("Getting element content for %s" % match)
                temp = _getDOMContent(item, name, match, ret).strip()
                item = item[item.find(temp, item.find(match)) + len(temp):]
                lst2.append(temp)
            lst = lst2
        ret_lst += lst

    # log_debug("Done: " + repr(ret_lst))
    return ret_lst


def _getDOMContent(html, name, match, ret):  # Cleanup
    # log_debug("match: " + match)

    endstr = u"</" + name  # + ">"

    start = html.find(match)
    end = html.find(endstr, start)
    pos = html.find("<" + name, start + 1 )

    # log_debug(str(start) + " < " + str(end) + ", pos = " + str(pos) + ", endpos: " + str(end))

    while pos < end and pos != -1:  # Ignore too early </endstr> return
        tend = html.find(endstr, end + len(endstr))
        if tend != -1:
            end = tend
        pos = html.find("<" + name, pos + 1)
        # log_debug("loop: " + str(start) + " < " + str(end) + " pos = " + str(pos))

    # log_debug("start: %s, len: %s, end: %s" % (start, len(match), end))
    if start == -1 and end == -1:
        result = u""
    elif start > -1 and end > -1:
        result = html[start + len(match):end]
    elif end > -1:
        result = html[:end]
    elif start > -1:
        result = html[start + len(match):]

    if ret:
        endstr = html[end:html.find(">", html.find(endstr)) + 1]
        result = match + result + endstr

    # log_debug("done result length: " + str(len(result)))
    return result


def _getDOMAttributes(match, name, ret):

    lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
    if len(lst) == 0:
        lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
    ret = []
    for tmp in lst:
        cont_char = tmp[0]
        if cont_char in "'\"":
            # log_debug("Using %s as quotation mark" % cont_char)

            # Limit down to next variable.
            if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
                tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]

            # Limit to the last quotation mark
            if tmp.rfind(cont_char, 1) > -1:
                tmp = tmp[1:tmp.rfind(cont_char)]
        else:
            # log_debug("No quotation mark found")
            if tmp.find(" ") > 0:
                tmp = tmp[:tmp.find(" ")]
            elif tmp.find("/") > 0:
                tmp = tmp[:tmp.find("/")]
            elif tmp.find(">") > 0:
                tmp = tmp[:tmp.find(">")]

        ret.append(tmp.strip())

    # log_debug("Done: " + repr(ret))
    return ret


def _getDOMElements(item, name, attrs):

    lst = []
    for key in attrs:
        lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
        if len(lst2) == 0 and attrs[key].find(" ") == -1:  # Try matching without quotation marks
            lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

        if len(lst) == 0:
            # log_debug("Setting main list " + repr(lst2))
            lst = lst2
            lst2 = []
        else:
            # log_debug("Setting new list " + repr(lst2))
            test = list(range(len(lst)))
            test.reverse()
            for i in test:  # Delete anything missing from the next list.
                if not lst[i] in lst2:
                    # log_debug("Purging mismatch " + str(len(lst)) + " - " + repr(lst[i]))
                    del(lst[i])

    if len(lst) == 0 and attrs == {}:
        # log_debug("No list found, trying to match on name only")
        lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
        if len(lst) == 0:
            lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)

    # log_debug("Done: " + str(type(lst)))
    return lst


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


def replaceHTMLCodes(txt):

    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    txt = txt.replace("&#38;", "&")
    txt = txt.replace("&nbsp;", "")

    return txt


def cfcookie(netloc, ua, timeout):
    try:
        headers = {'User-Agent': ua}

        req = urllib2.Request(netloc, headers=headers)

        try:
            urllib2.urlopen(req, timeout=int(timeout))
        except urllib2.HTTPError as response:
            result = response.read(5242880)

        jschl = re.findall('name="jschl_vc" value="(.+?)"/>', result)[0]

        init = re.findall('setTimeout\(function\(\){\s*.*?.*:(.*?)};', result)[-1]

        builder = re.findall(r"challenge-form\'\);\s*(.*)a.v", result)[0]

        decryptVal = parseJSString(init)

        lines = builder.split(';')

        for line in lines:

            if len(line) > 0 and '=' in line:

                sections = line.split('=')
                line_val = parseJSString(sections[1])
                decryptVal = int(eval(str(decryptVal) + str(sections[0][-1]) + str(line_val)))

        answer = decryptVal + len(urlparse(netloc).netloc)

        query = '%s/cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s' % (netloc, jschl, answer)

        if 'type="hidden" name="pass"' in result:
            passval = re.findall('name="pass" value="(.*?)"', result)[0]
            query = '%s/cdn-cgi/l/chk_jschl?pass=%s&jschl_vc=%s&jschl_answer=%s' % (
                netloc, quote_plus(passval), jschl, answer
            )
            time.sleep(5)

        cookies = cookielib.LWPCookieJar()
        handlers = [urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(cookies)]
        opener = urllib2.build_opener(*handlers)
        urllib2.install_opener(opener)

        try:
            req = urllib2.Request(query, headers=headers)
            urllib2.urlopen(req, timeout=int(timeout))
        except Exception:
            pass

        cookie = '; '.join(['%s=%s' % (i.name, i.value) for i in cookies])

        return cookie
    except Exception:
        pass


def parseJSString(s):
    try:
        offset = 1 if s[0] == '+' else 0
        val = int(eval(s.replace('!+[]', '1').replace('!![]', '1').replace('[]','0').replace('(', 'str(')[offset:]))
        return val
    except Exception:
        pass
