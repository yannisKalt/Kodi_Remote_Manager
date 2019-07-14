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
from __future__ import absolute_import

import re, unicodedata
from tulip.compat import unicode


def get(title, lower=True):

    if title is None:
        return

    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = re.sub(r'\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title)

    if lower:

        title = title.lower()

    return title


def replace_xml_codes(title):

    title = unicode(title)

    title = title.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&Amp;', '&')
    title = title.replace('&#34;', '”').replace('&#39;', "'").replace('&#039;', "'").replace('&quot;', '"')
    title = title.replace('&Quot;', '"').replace('&szlig;', 'ß').replace('&mdash;', '-').replace('&ndash;', '-')
    title = title.replace('–', '-').replace('&#x00c4', 'Ä').replace('&#x00e4', 'ä').replace('&#x00d6', 'Ö')
    title = title.replace('&#x00f6', 'ö').replace('&#x00dc', 'Ü').replace('&#x00fc', 'ü').replace('&#x00df', 'ß')
    title = title.replace('&Auml;', 'Ä').replace('&auml;', 'ä').replace('&Euml;', 'Ë').replace('&euml;', 'ë')
    title = title.replace('&Iuml;', 'Ï').replace('&iuml;', 'ï').replace('&Ouml;', 'Ö').replace('&ouml;', 'ö')
    title = title.replace('&Uuml;', 'Ü').replace('&uuml;', 'ü').replace('&#376;', 'Ÿ').replace('&yuml;', 'ÿ')
    title = title.replace('&agrave;', 'à').replace('&Agrave;', 'À').replace('&aacute;', 'á').replace('&Aacute;', 'Á')
    title = title.replace('&egrave;', 'è').replace('&Egrave;', 'È').replace('&eacute;', 'é').replace('&Eacute;', 'É')
    title = title.replace('&igrave;', 'ì').replace('&Igrave;', 'Ì').replace('&iacute;', 'í').replace('&Iacute;', 'Í')
    title = title.replace('&ograve;', 'ò').replace('&Ograve;', 'Ò').replace('&oacute;', 'ó').replace('&Oacute;', 'ó')
    title = title.replace('&ugrave;', 'ù').replace('&Ugrave;', 'Ù').replace('&uacute;', 'ú').replace('&Uacute;', 'Ú')
    title = title.replace('&yacute;', 'ý').replace('&Yacute;', 'Ý').replace('&atilde;', 'ã').replace('&Atilde;', 'Ã')
    title = title.replace('&ntilde;', 'ñ').replace('&Ntilde;', 'Ñ').replace('&otilde;', 'õ').replace('&Otilde;', 'Õ')
    title = title.replace('&Scaron;', 'Š').replace('&scaron;', 'š').replace('™', '')
    title = title.replace('&acirc;', 'â').replace('&Acirc;', 'Â').replace('&ccedil;', 'ç').replace('&Ccedil;', 'Ç')
    title = title.replace('&ecirc;', 'ê').replace('&Ecirc;', 'Ê').replace('&icirc;', 'î').replace('&Icirc;', 'Î')
    title = title.replace('&ocirc;', 'ô').replace('&Ocirc;', 'Ô').replace('&ucirc;', 'û').replace('&Ucirc;', 'Û')
    title = title.replace('&alpha;', 'a').replace('&Alpha;', 'A').replace('&aring;', 'å').replace('&Aring;', 'Å')
    title = title.replace('&aelig;', 'æ').replace('&AElig;', 'Æ').replace('&epsilon;', 'e').replace('&Epsilon;', 'Ε')
    title = title.replace('&eth;', 'ð').replace('&ETH;', 'Ð').replace('&gamma;', 'g').replace('&Gamma;', 'G')
    title = title.replace('&oslash;', 'ø').replace('&Oslash;', 'Ø').replace('&theta;', 'θ').replace('&thorn;', 'þ')
    title = title.replace('&THORN;', 'Þ').replace('&x27;', '\'').replace('&bull;', '•').replace('&iexcl;', '¡')
    title = title.replace('&iquest;', '¿').replace('&rsquo;', '’').replace('&lsquo;', '‘').replace('&sbquo;', '’')
    title = title.replace('&rdquo;', '”').replace('&ldquo;', '“').replace('&bdquo;', '”').replace('&rsaquo;', '›')
    title = title.replace('lsaquo;', '‹').replace('&raquo;', '»').replace('&laquo;', '«').replace('&copy;', '©')
    title = title.replace('&reg;', '®')

    title = title.strip()

    return title


def replace_feat(title):

    title = title.replace('Ft.', 'feat.')
    title = title.replace(' ft ', ' feat. ').replace(' FT ', ' feat. ').replace(' Ft ', ' feat. ')
    title = title.replace('ft.', 'feat.').replace(' FEAT ', ' feat. ').replace(' Feat ', ' feat. ')
    title = title.replace('Feat.', 'feat.').replace('Featuring', 'feat.')

    return title


def query(title):

    if title is None:
        return

    title = title.replace("'", '').rsplit(':', 1)[0]

    return title


def normalize(title):

    try:

        try:
            return title.decode('ascii').encode('utf-8')
        except Exception:
            pass

        t = ''
        for i in title:
            c = unicodedata.normalize('NFKD', unicode(i, 'ISO-8859-1'))
            c = c.encode('ascii', 'ignore').strip()
            if i == ' ':
                c = i
            t += c

        return t.encode('utf-8')

    except Exception:

        return title


def strip_accents(string):

    result = ''.join(c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn')

    return result
