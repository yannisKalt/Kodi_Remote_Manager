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

from xbmcvfs import rename, File as openFile
import re, zipfile
from os.path import split as os_split
from resources.lib.tools import multichoice
from tulip.compat import urljoin, quote_plus, unquote_plus, quote
from tulip import cache, cleantitle, client, control, log


class subzxyz:

    def __init__(self):

        self.list = [] ; self.data = []

    def get(self, query):

        try:

            try:
                match = re.findall(r'(.+?) (?!\d{4})S?(\d{1,2}) ?X?E?(\d{1,2})$', query, flags=re.IGNORECASE)[0]
            except Exception:
                match = None

            if not match:

                match = re.findall(r'(.+?) *?\(?(\d{4})?\)?$', query)[0]

                if len(match[1]) == 4:

                    title, year = match[0], match[1]

                else:

                    title = match[0]

                query = ' '.join(unquote_plus(re.sub('%\w\w', ' ', quote_plus(title))).split())

                url = 'https://subz.xyz/search?q={0}'.format(quote_plus(query))

                result = client.request(url)
                result = re.sub(r'[^\x00-\x7F]+', ' ', result)

                url = client.parseDOM(result, 'section', attrs={'class': 'movies'})[0]
                url = re.findall('(/movies/\d+)', url)
                url = [x for y, x in enumerate(url) if x not in url[:y]]
                url = [urljoin('https://subz.xyz', i) for i in url]
                url = url[:20][::-1]

                for i in url:

                    c = cache.get(self.cache, 2200, i)

                    if c is not None:

                        if len(match[1]) == 4:
                            year_check = c[1] == year
                        else:
                            year_check = True

                        if cleantitle.get(c[0]) == cleantitle.get(title) and year_check:

                            try:

                                item = self.r

                            except Exception:

                                item = client.request(i)

                            break

                        else:

                            self.data.append(self.r)

            else:

                title, season, episode = match

                season, episode = '{0}'.format(season), '{0}'.format(episode)

                query = ' '.join(unquote_plus(re.sub('%\w\w', ' ', quote_plus(title))).split())

                url = 'https://subz.xyz/search?q={0}'.format(quote_plus(query))

                result = client.request(url)
                result = re.sub(r'[^\x00-\x7F]+', ' ', result)

                url = client.parseDOM(result, 'section', attrs={'class': 'tvshows'})[0]
                url = re.findall('(/series/\d+)', url)
                url = [x for y, x in enumerate(url) if x not in url[:y]]
                url = [urljoin('https://subz.xyz', i) for i in url]
                url = url[:20][::-1]

                for i in url:

                    c = cache.get(self.cache, 2200, i)

                    if c is not None:

                        if cleantitle.get(c[0]) == cleantitle.get(title):

                            item = i

                            break

                item = '{0}/seasons/{1}/episodes/{2}'.format(item, season, episode)
                item = client.request(item)

            if self.data:

                item = '\n\n'.join(self.data)

            item = re.sub(r'[^\x00-\x7F]+', ' ', item)
            items = client.parseDOM(item, 'tr', attrs={'data-id': '.+?'})

        except Exception as e:

            log.log('Subzxyz failed at get function, reason: ' + str(e))

            return

        for item in items:

            try:

                r = client.parseDOM(item, 'td', attrs={'class': '.+?'})[-1]

                url = client.parseDOM(r, 'a', ret='href')[0]
                url = client.replaceHTMLCodes(url)
                url = url.replace("'", "").encode('utf-8')

                name = url.split('/')[-1].strip()
                name = re.sub('\s\s+', ' ', name)
                name = name.replace('_', '').replace('%20', '.')
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'source': 'subzxyz', 'rating': 5})

            except Exception as e:

                log.log('Subzxyz failed at self.list formation function, reason: ' + str(e))

                return

        return self.list

    def cache(self, i):

        try:

            self.r = client.request(i)
            self.r = re.sub(r'[^\x00-\x7F]+', ' ', self.r)
            t = re.findall(r'(?:\"|\')original_title(?:\"|\')\s*:\s*(?:\"|\')(.+?)(?:\"|\')', self.r)[0]
            y = re.findall(r'(?:\"|\')year(?:\"|\')\s*:\s*(?:\"|\'|)(\d{4})', self.r)[0]

            return t, y

        except Exception as e:

            log.log('Subzxyz failed at cache function, reason: ' + str(e))

            return

    @staticmethod
    def download(path, url):

        try:

            result = client.request(url)

            f = control.join(path, os_split(url)[1])

            with open(f, 'wb') as subFile:
                subFile.write(result)

            dirs, files = control.listDir(path)

            if len(files) == 0:
                return

            if not f.lower().endswith('.rar'):

                try:
                    zipped = zipfile.ZipFile(f)
                    zipped.extractall(path)
                except Exception:
                    control.execute('Extract("{0}","{0}")'.format(f, path))

            if f.lower().endswith('.rar'):

                if control.infoLabel('System.Platform.Windows'):
                    uri = "rar://{0}/".format(quote(f))
                else:
                    uri = "rar://{0}/".format(quote_plus(f))

                dirs, files = control.listDir(uri)

            else:

                dirs, files = control.listDir(path)

            if dirs and f.lower().endswith('.rar'):

                for dir in dirs:

                    _dirs, _files = control.listDir(control.join(uri, dir))

                    [files.append(control.join(dir, i)) for i in _files]

                    if _dirs:

                        for _dir in _dirs:
                            _dir = control.join(_dir, dir)

                            __dirs, __files = control.listDir(
                                control.join(uri, _dir)
                            )

                            [files.append(control.join(_dir, i)) for i in __files]

            filenames = [i for i in files if i.endswith(('.srt', '.sub'))]

            if len(filenames) == 1:
                filename = filenames[0]
            else:
                filename = multichoice(filenames)

            try:

                filename = filename.decode('utf-8')

            except Exception:

                pass

            if not control.exists(control.join(path, os_split(filename)[0])) and f.lower().endswith('.rar'):
                control.makeFiles(control.join(path, os_split(filename)[0]))

            subtitle = control.join(path, filename)

            if f.lower().endswith('.rar'):

                content = openFile(uri + filename).read()

                with open(subtitle, 'wb') as subFile:
                    subFile.write(content)

            fileparts = os_split(subtitle)[1].split('.')
            result = control.join(os_split(subtitle)[0], 'subtitles.' + fileparts[len(fileparts)-1])

            rename(subtitle, result)

            return result

        except Exception as e:

            log.log('Subzxyz subtitle download failed for the following reason: ' + str(e))

            return
