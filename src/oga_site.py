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

class ContentSite(object):

    def __init__(self, url):
        """

        Arguments:
        - `url`:
        """
        self.url = url
        self.title = ""
        self.author = ""
        self.date_string = ""
        self.date = None
        self.body = ""
        self.attr_instructions = "No specific instructions given"
        self.art_type = -1
        self.art_type_string = ""
        self.tags = []
        self.licenses = []
        self.files = {}
        self.comments = []

        self.preview_ogg_url = ""
        self.preview_mp3_url = ""

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_art_type_str(self):
        return self.art_type_string

    def get_date_string(self):
        return self.date_string

    def get_body(self):
        return self.body

    def get_files(self):
        return self.files

    def get_licenses(self):
        return self.licenses

    def get_attr_instructions(self):
        return self.attr_instructions
