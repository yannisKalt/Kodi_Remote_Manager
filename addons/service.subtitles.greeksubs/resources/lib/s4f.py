# -*- coding: utf-8 -*-

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import xbmc
import urllib, urlparse, re, os, requests
from resources.modules import client
from resources.modules import control


class s4f:
    def __init__(self):
        self.list = []
        self.base_link = 'https://www.sf4-industry.com'
        self.base_TVlink = 'https://www.subs4series.com'
        self.search = 'search_report.php?search=%s&searchType=1'

    def get(self, query):
        try:
            query, imdb = query.split('/imdb=')
            match = re.findall(r'^(?P<title>.+)[\s+\(|\s+](?P<year>\d{4})', query)
            # xbmc.log('$#$MATCH-S4F: %s' % match, xbmc.LOGNOTICE)

            if len(match) > 0:
                hdr = {
                    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
                    'Referer': 'https://www.subs4free.info/'}

                title, year = match[0][0], match[0][1]

                query = urllib.quote_plus('{} {}'.format(title, year))

                url = urlparse.urljoin(self.base_link, self.search % query)

                req = requests.get(url, headers=hdr)
                cj = req.cookies
                r = req.content
                r = re.sub(r'[^\x00-\x7F]+', ' ', r)
                # xbmc.log('$#$HTML: %s' % r, xbmc.LOGNOTICE)

                urls = client.parseDOM(r, 'div', attrs={'class': 'movie-download'})
                # urls += client.parseDOM(r, 'div', attrs={'class': ' seeMedium'})
                # xbmc.log('$#$URLS-start: %s' % urls, xbmc.LOGNOTICE)
                urls = [i for i in urls if '/greek-sub' in i]
                # urls = [(client.parseDOM(i, 'tr')[0], re.findall(r'<b>(\d+)</b>DLs', i, re.I)[0]) for i in urls if i]
                urls = [(client.parseDOM(i, 'a', ret='href')[0],
                         client.parseDOM(i, 'a', ret='title')[0],
                         re.findall(r'<b>(\d+)</b>DLs', i, re.I)[0]) for i in urls if i]
                # xbmc.log('$#$URLS: %s' % urls, xbmc.LOGNOTICE)
                urls = [(urlparse.urljoin(self.base_link, i[0]), i[1].split('for ', 1)[1],
                         i[2]) for i in urls if i]
                urls = [(i[0], i[1], i[2]) for i in urls if i]
                # xbmc.log('$#$URLS: %s' % urls, xbmc.LOGNOTICE)


            else:
                hdr = {
                    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
                    'Referer': 'https://www.subs4series.com/'}
                title, hdlr = re.findall(r'^(?P<title>.+)\s+(?P<hdlr>S\d+E\d+)', query, re.I)[0]
                # xbmc.log('$#$MATCH-S4F: %s | %s' % (title, hdlr), xbmc.LOGNOTICE)

                # hdlr = 'S%02dE%02d' % (int(season), int(episode))

                query = urllib.quote('{} {}'.format(title, hdlr))

                url = urlparse.urljoin(self.base_TVlink, self.search % query)

                req = requests.get(url, headers=hdr)

                cj = req.cookies
                r = req.content
                r = re.sub(r'[^\x00-\x7F]+', ' ', r)
                # xbmc.log('@@URL:%s' % r)

                urls = client.parseDOM(r, 'div', attrs={'class': ' seeDark'})
                urls += client.parseDOM(r, 'div', attrs={'class': ' seeMedium'})
                urls = [i for i in urls if not '/en.gif' in i]
                urls = [(client.parseDOM(i, 'tr')[0], re.findall(r'<B>(\d+)</B>DLs', i, re.I)[0]) for i in urls if i]
                urls = [(client.parseDOM(i[0], 'a', ret='href')[0],
                         client.parseDOM(i[0], 'a', ret='title')[0], i[1]) for i in urls if i]
                urls = [(urlparse.urljoin(self.base_TVlink, i[0]), re.sub('Greek subtitle[s] for ', '', i[1]),
                         i[2]) for i in urls if i]
                urls = [(i[0], i[1], i[2]) for i in urls if i]

        except BaseException:
            return

        for i in urls:
            try:
                rating = self._rating(i[2])
                name = i[1].replace('_', '').replace('%20', '.')
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = i[0]
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': '{}|{}|{}'.format(url, cj['PHPSESSID'], cj['__cfduid']),
                                  'source': 's4f', 'rating': rating})
            except BaseException:
                pass

        return self.list

    def _rating(self, downloads):

        try:
            rating = int(downloads)
        except BaseException:
            rating = 0

        if rating < 100:
            rating = 1
        elif rating >= 100 and rating < 200:
            rating = 2
        elif rating >= 200 and rating < 300:
            rating = 3
        elif rating >= 300 and rating < 400:
            rating = 4
        elif rating >= 400:
            rating = 5

        return rating

    def download(self, path, url):

        try:
            url, php, cfd = url.split('|')
            if 'subs4series' in url:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
                    'Referer': url,
                    'Origin': 'https://www.subs4series.com/'}
                cj = {'PHPSESSID': php,
                      '__cfduid': cfd}

                r = requests.get(url, headers=headers, cookies=cj).content
                r = re.sub(r'[^\x00-\x7F]+', ' ', r)
                # xbmc.log('@@HTML:%s' % r)

                pos = re.findall(r'\/(getSub-\w+\.html)', r, re.I | re.DOTALL)[0]
                # xbmc.log('@@POSSSSS:%s' % pos)
                post_url = urlparse.urljoin(self.base_TVlink, pos)
                # xbmc.log('@@POStttt:%s' % post_url)
                r = requests.get(post_url, headers=headers, cookies=cj)
                surl = r.url
                result = client.request(surl)


            else:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
                    'Referer': url,
                    'Origin': 'https://www.sf4-industry.com'}
                cj = {'PHPSESSID': php,
                      '__cfduid': cfd}
                post_url = 'https://www.sf4-industry.com/getSub.php'

                r = requests.get(url, headers=headers, cookies=cj).text
                r = re.sub(r'[^\x00-\x7F]+', ' ', r)
                # xbmc.log('@@HTMLLL:%s' % r)
                pos = client.parseDOM(r, 'div', attrs={'class': 'download-btn'})[0]
                pos = client.parseDOM(pos, 'input', ret='value', attrs={'name': 'id'})[0]
                # pos = re.findall(r'getSub-(\w+)\.html', r, re.I | re.DOTALL)[0]
                post = {'id': pos,
                        'x': '107',
                        'y': '35'}

                r = requests.post(post_url, headers=headers, data=post, cookies=cj)
                # surl = r.headers['Location']
                surl = r.url
                result = client.request(surl)
                # surl = self.base_link + surl if surl.startswith('/') else surl

            f = os.path.join(path, surl.rpartition('/')[2])
            if f.lower().endswith('.rar') and not control.condVisibility('system.platform.osx'):
                return control.okDialog('GreekSubs', 'Το αρχείο υποτίτλου είναι σε μορφή rar\n και δεν μπορεί να ληφθεί.\n'
                                        'Δοκιμάστε άλλον υπότιτλο!')

            with open(f, 'wb') as subFile:
                subFile.write(result)

            dirs, files = control.listDir(path)

            if len(files) == 0:
                return

            if not f.lower().endswith('.rar'):
                control.execute('Extract("{}","{}")'.format(f, path))

            if control.condVisibility('system.platform.windows'):
                conversion = urllib.quote
            else:
                conversion = urllib.quote_plus

            if f.lower().endswith('.rar'):
                if control.condVisibility('system.platform.osx'):
                    uri = "rar://{0}/".format(conversion(f))
                    dirs, files = control.listDir(uri)
                else:
                    return

            else:

                for i in range(0, 10):

                    try:
                        dirs, files = control.listDir(path)
                        if len(files) > 1:
                            break
                        if control.aborted is True:
                            break
                        control.wait(1)
                    except BaseException:
                        pass

            filenames = [i for i in files if any(i.endswith(x) for x in ['.srt', '.sub'])]

            if len(filenames) == 1:
                filename = filenames[0]
            else:
                filename = multichoice(filenames)

            try:
                filename = filename.decode('utf-8')
            except BaseException:
                pass

            subtitle = os.path.join(path, filename)

            if f.lower().endswith('.rar'):

                content = control.openFile(path + filename).read()

                with open(subtitle, 'w') as subFile:
                    subFile.write(content)

                control.deleteFile(f)
                return subtitle

            else:

                return subtitle

        except BaseException:
            pass


def multichoice(filenames, allow_random=False):
    from random import choice
    from os.path import split as os_split
    if filenames is None or len(filenames) == 0:

        return

    elif len(filenames) >= 1:

        if allow_random:
            length = len(filenames) + 1
        else:
            length = len(filenames)

        if len(filenames) == 1:
            return filenames[0]

        choices = [os_split(i)[1] for i in filenames]

        if allow_random:
            choices.insert(0, control.lang(32215))

        _choice = control.selectDialog(heading=control.lang(32214), list=choices)

        if _choice == 0:
            if allow_random:
                filename = choice(filenames)
            else:
                filename = filenames[0]
        elif _choice != -1 and _choice <= length:
            if allow_random:
                filename = filenames[_choice - 1]
            else:
                filename = filenames[_choice]
        else:
            if allow_random:
                filename = choice(filenames)
            else:
                return

        return filename

    else:

        return