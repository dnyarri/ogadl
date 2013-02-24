import string
import textwrap

from PyQt4.QtCore import QFile, QIODevice

LINE_LENGTH = 79


class InfoGenerator(object):
    """
    """

    def __init__(self):
        """
        """
        self.template = None

    def read_template(self, path):
        """

        Arguments:
        - `path`:
        """
        # if not QFile.exists(path):
        #     # TODO: Show messagebox to user and open file dialog
        #     return

        # f = QFile(path)
        # if not f.open(QIODevice.ReadOnly | QIODevice.Text):
        #     # TODO: Show messagebox
        #     return
        with open(path) as f:
            self.template = string.Template(f.read())


    def make_info(self, **kwargs):
        """

        Arguments:
        - `**kwargs`:
        """
        values = {}
        values['title'] = kwargs['title']
        values['author'] = kwargs['author']
        file_names = kwargs['file_names']
        values['file_names'] = '\n'.join(file_names)
        values['body'] = textwrap.fill(kwargs.get('body', 'No description'),
                                       width=LINE_LENGTH)
        attr_instructions = kwargs.get('attr_instructions', 'No specific instructions')
        values['attr_instructions'] = textwrap.fill(attr_instructions,
                                                    width=LINE_LENGTH)
        values['art_type'] = kwargs.get('art_type', 'Not specified')
        licenses = kwargs.get('licenses', ['License reading not implemented'])
        values['licenses'] = '\n'.join(licenses)

        result = self.template.substitute(values)

        return result
