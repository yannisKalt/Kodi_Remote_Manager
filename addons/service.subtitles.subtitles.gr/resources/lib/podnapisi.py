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


class Podnapisi:

    def __init__(self):

        self.list = []
        self.base_link = 'https://www.podnapisi.net'
        self.search_link = ''.join([self.base_link, '/en/subtitles/search/'])

    def get(self, query):

        try:

            query = ' '.join(unquote_plus(re.sub(r'%\w\w', ' ', quote_plus(query))).split())

            query_link = '&'.join(
                [
                    'keywords={keywords}', 'movie_type={movie_type}', 'language=!el', 'seasons={seasons}',
                    'episodes={episodes}', 'year={year}', 'type=', 'undefined=auto', 'undefined=en'
                ]
            )

            match = re.findall(
                r'(.+?)(?: -)? (?:\(?(\d{4})\)?|S?(\d{1,2})X? ?E?P?(\d{1,2})(?: \. (.+))?)', query, flags=re.I
            )

            if match:

                query, year, season, episode, episode_title = match[0]

                url = '?'.join(
                    [
                        self.search_link,
                        query_link.format(
                            keywords=quote_plus(query),
                            movie_type='movie' if year and not (season or episode) else 'tv-series',
                            seasons=season, episodes=episode, year=year
                        )
                    ]
                )

            else:

                url = '?'.join(
                    [
                        self.search_link,
                        query_link.format(
                            keywords=quote_plus(query), movie_type='', seasons='', episodes='', year=''
                        )
                    ]
                )

            result = client.request(url, headers={'Accept': 'text/html', 'Accept-Language': 'en-US,en;q=0.9,el;q=0.8'})

            try:
                result = result.decode('utf-8', errors='replace')
            except AttributeError:
                pass

            items = client.parseDOM(result, 'tr', attrs={'class': 'subtitle-entry'})

        except Exception as e:

            _, __, tb = sys.exc_info()

            print(traceback.print_tb(tb))

            log.log('Podnapisi.net failed at get function, reason: ' + str(e))

            return

        for item in items:

            try:

                if '<span>el</span>' not in item:
                    continue

                table = client.parseDOM(item, 'td')

                try:
                    downloads = [i.strip() for i in table]
                    downloads = [i for i in downloads if i.isdigit()][1]
                except IndexError:
                    downloads = '0'

                downloads = re.sub('[^0-9]', '', downloads)

                label = client.parseDOM(item, 'a', attrs={'alt': 'Subtitles\' page'})[0]
                label = client.replaceHTMLCodes(label)
                name = u'{0} [{1} DLs]'.format(label, downloads)

                url = [i for i in table if 'Download subtitles.' in i][0]
                url = client.parseDOM(url, 'a', ret='href')[0]
                url = ''.join([self.base_link, url])

                rating = [i for i in table if 'progress rating' in i][0]
                rating = client.parseDOM(rating, 'div', attrs={'class': 'progress rating'}, ret='data-title')[0]
                rating = int(rating.partition('.')[0]) / 20

                self.list.append(
                    {
                        'name': name, 'url': url, 'source': 'podnapisi', 'rating': rating, 'title': label,
                        'downloads': downloads
                    }
                )

            except Exception as e:

                _, __, tb = sys.exc_info()

                print(traceback.print_tb(tb))

                log.log('Podnapisi.net failed at self.list formation function, reason: ' + str(e))

                return

        return self.list

    def download(self, path, url):

        filename = '.'.join(urlparse(url).path.split('/')[3:5] + ['zip'])
        filename = control.join(path, filename)

        try:

            client.retriever(url, filename)

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

            log.log('Podnapisi.net subtitle download failed for the following reason: ' + str(e))

            return
