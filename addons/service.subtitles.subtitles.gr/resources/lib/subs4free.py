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

from __future__ import print_function, division

from contextlib import closing
import zipfile, re, sys, traceback
from tulip import control, client, log
from tulip.compat import unquote_plus, quote_plus, urlparse


class Subs4free:

    def __init__(self):

        self.list = []
        self.base_link = 'https://www.sf4-industry.com'
        self.series_link = 'https://www.subs4series.com'
        self.download_link = ''.join([self.base_link, '/getSub.html'])
        self.search_link = ''.join([self.base_link, '/search_report.php'])

    def get(self, query):

        try:

            query = ' '.join(unquote_plus(re.sub(r'%\w\w', ' ', quote_plus(query))).split())

            query_link = '&'.join(
                [
                    'search={query}', 'searchType={search_type}'
                ]
            )

            if re.search(r'\(?\d{4}\)?', query):
                search_type = '1'
            else:
                search_type = '2'

            url = '?'.join(
                [
                    self.search_link,
                    query_link.format(query=quote_plus(query), search_type=search_type
                    )
                ]
            )

            try:
                result = client.request(url).decode('iso-8859-7').encode('utf-8')
            except Exception:
                result = client.request(url)

            items = client.parseDOM(result, 'div', attrs={'onMouseOver': "this.className='highlight'"})

        except Exception as e:

            _, __, tb = sys.exc_info()

            print(traceback.print_tb(tb))

            log.log('Subs4free.info failed at get function, reason: ' + str(e))

            return

        for item in items:

            try:

                if 'el.gif' not in item:
                    continue

                label, uploader, downloads = client.parseDOM(item, 'B')

                downloads = re.sub('[^0-9]', '', downloads)

                name = u'{0} [{1} DLs]'.format(label, downloads)

                try:
                    url = client.parseDOM(item, 'a', attrs={'rel': 'nofollow'}, ret='href')[0]
                    url = ''.join([self.base_link, url])
                except IndexError:
                    url = client.parseDOM(item, 'a', attrs={'title': 'Greek subtitles for.+?'}, ret='href')[0]
                    url = ''.join([self.series_link, url])

                rating = self._rating(downloads)

                self.list.append(
                    {
                        'name': label, 'url': url, 'source': 'subs4free', 'rating': rating, 'title': name,
                        'downloads': downloads
                    }
                )

            except Exception as e:

                _, __, tb = sys.exc_info()

                print(traceback.print_tb(tb))

                log.log('Subs4free.info failed at self.list formation function, reason: ' + str(e))

                return

        return self.list

    def _rating(self, downloads):

        try:

            rating = int(downloads)

        except:

            rating = 0

        if rating < 500:
            rating = 1
        elif 500 <= rating < 1000:
            rating = 2
        elif 1000 <= rating < 1500:
            rating = 3
        elif 1500 <= rating < 2000:
            rating = 4
        elif rating >= 2000:
            rating = 5

        return rating

    def download(self, path, url):

        cookie = client.request(url, output='cookie', close=False)

        try:
            html = client.request(url, cookie=cookie).decode('iso-8859-7').encode('utf-8')
        except Exception:
            html = client.request(url, cookie=cookie)

        try:
            sub_id = '='.join(['id', client.parseDOM(html, 'input', attrs={'type': 'hidden'}, ret='value')[0]])
            sub = client.request(url, post=sub_id, output='geturl', cookie=cookie, headers={'Referer': url})
        except IndexError:
            get_link = client.parseDOM(html, 'a', attrs={'rel': 'nofollow', 'class': 'style55ws'}, ret='href')[0]
            sub = client.request(''.join([self.series_link, get_link]), output='geturl', cookie=cookie, headers={'Referer': url})

        try:

            filename = urlparse(sub).path.split('/')[-1]
            filename = control.join(path, filename)

            client.retriever(sub, filename)

            zip_file = zipfile.ZipFile(filename)
            files = zip_file.namelist()
            srt = [i for i in files if i.endswith(('.srt', '.sub'))][0]
            subtitle = control.join(path, srt)

            try:
                zipped = zipfile.ZipFile(filename)
                zipped.extractall(filename)
            except Exception:
                control.execute('Extract("{0}","{1}")'.format(filename, path))

            with closing(control.openFile(subtitle)) as fn:

                try:
                    output = bytes(fn.readBytes())
                except Exception:
                    output = bytes(fn.read())

            content = output.decode('utf-16')

            with closing(control.openFile(subtitle, 'w')) as subFile:
                subFile.write(bytearray(content.encode('utf-8')))

            return subtitle

        except Exception as e:

            _, __, tb = sys.exc_info()

            print(traceback.print_tb(tb))

            log.log('Subs4free.info subtitle download failed for the following reason: ' + str(e))

            return
