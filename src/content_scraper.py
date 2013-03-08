# This file is part of ogadl.

# ogadl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ogadl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ogadl.  If not, see <http://www.gnu.org/licenses/>.

import urllib.request

import bs4
from PyQt4.QtCore import QUrl

import oga_site

ART_2D = 0
ART_3D = 1
ART_CONCEPT = 2
ART_TEXTURE = 3
ART_MUSIC = 4
ART_SFX = 5
ART_DOCUMENT = 6

URL_OGA = 'opengameart.org'


class ContentScraper(object):
    """ This class scrapes content pages like
    opengameart.org/content/kawarayu

    """

    def read_data(self, url):
        """ Reads data from website and saves them to variables which you can
        get by using corresponding method.
        """
        if not url.startswith('http://'):
            url = 'http://' + url

        page_response = urllib.request.urlopen(url)
        page = page_response.read()
        soup = bs4.BeautifulSoup(page)
        content_div = soup.find('div', id='block-system-main')

        site = oga_site.ContentSite(url)

        title_div = content_div.find('div', {'property': 'dc:title'})
        site.title = title_div.contents[0].string

        span_username = content_div.find('span', {'class': 'username'})
        site.author = span_username.contents[0].string

        # TODO: Add compatibility code for texture-pages
        art_type_div = content_div.find('div',
                                        {'class': 'field-name-field-art-type'})
        site.art_type_string = art_type_div.select('div > div > a')[0].string
        site.art_type = self._match_string_with_art_type(site.art_type_string)

        license_divs = content_div.find_all('div', {'class': 'license-name'})
        site.licenses = [lic_div.string for lic_div in license_divs]

        files_div = content_div.find('div',
                                     {'class': 'field-name-field-art-files'})
        files_links = files_div.select('a')
        site.files = {link.string: QUrl.fromEncoded('http://' + URL_OGA + link['href'])
                      for link in files_links}

        for key, val in site.files.items():
            site.files[key] = QUrl.fromEncoded(val.queryItemValue('file'))

        date_div = content_div.find('div', {'class': 'field-name-post-date'})
        site.date_string = date_div.select('div > div')[0].string

        body_div = content_div.find('div', {'class': 'field-name-body'})
        body_strings = body_div.select('div p')[0].strings
        site.body = ' '.join(list(body_strings))

        attr_instruction_div = content_div.find(
            'div', {'class': 'field-name-field-art-attribution'})
        if attr_instruction_div:
            site.attr_instructions = attr_instruction_div.select('div > div')[0].string

        return site

    @staticmethod
    def _match_string_with_art_type(string):
        if string == "2D Art":
            return ART_2D
        elif string == "3D Art":
            return ART_3D
        elif string == "Concept Art":
            return ART_CONCEPT
        elif string == "Music":
            return ART_MUSIC
        elif string == "Sound Effect":
            return ART_SFX
        elif string == "Document":
            return ART_DOCUMENT
