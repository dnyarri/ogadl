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

import sys
import urllib.request

import bs4
from ui import ui_main
from PyQt4.QtGui import (QApplication, QWidget, QMainWindow, QFileDialog,
                         QMessageBox)
from PyQt4.QtCore import QFile, QFileInfo, QTextStream, QIODevice, QEventLoop
from PyQt4 import QtCore, QtNetwork
from PyQt4.QtNetwork import QNetworkReply

import content_scraper


class MyApp(QMainWindow, ui_main.Ui_MainWindow):
    """
    """

    def __init__(self):
        """
        """
        QMainWindow.__init__(self)
        ui_main.Ui_MainWindow.__init__(self)
        self.scraper = content_scraper.ContentScraper()
        self.sites = {}
        self.active_site = None
        self.setupUi(self)
        self.manager = QtNetwork.QNetworkAccessManager()
        self.replies = []
        self.current_path = None
        self.setup_signal_slots()


    def setup_signal_slots(self):
        self.btn_get.clicked.connect(self.get)
        self.btn_download.clicked.connect(self.download_selected)
        # self.manager.finished[QNetworkReply].connect(self.download_finished)

    def clear(self):
        pass

    def get(self):
        site = self.scraper.read_data(self.linein_url.text())
        self.sites[site.title] = site
        self.active_site = site

        self.lbl_title.setText(self.active_site.get_title())
        self.lbl_author.setText(self.active_site.get_author())
        self.lbl_art_type.setText(self.active_site.get_art_type_string())
        self.lbl_date.setText(self.active_site.get_date_string())
        self.lbl_description.setText(self.active_site.get_body())

        for f in self.active_site.get_files().keys():
            self.list_files.addItem(f)

    def download_selected(self):
        """
        """
        selected = self.list_files.selectedItems()
        selected = [selection.text() for selection in selected]

        urls = [self.active_site.get_files()[sel] for sel in selected]


        # TODO: Enable this stuff later

        self.current_path = QFileDialog.getExistingDirectory(self,
                                                             caption='Choose save folder',
                                                             directory='.')
        if self.current_path:
            info_file = QFile(self.current_path + "/info")
            if not info_file.open(QFile.WriteOnly | QFile.Text):
                QMessageBox.information(self, self.tr("Something"),
                                        self.tr("Could not open or create info"
                                        "file for editing"))
                info_file = None
            else:
                # out = QTextStream(info_file)
                # out << "Title: " << scraper.get_title() \
                #     << "\nAuthor: " << scraper.get_author() \
                #     << "\nArt type: " <<
                #     scraper.get_art_type_string()
                pass
        else:
            print(self.current_path)



        print(urls)
        for url in urls:


            request = QtNetwork.QNetworkRequest(url)
            reply = self.manager.get(request)
            # self.replies.append(reply)
            # loop = QEventLoop()
            reply.finished.connect(self.download_finished)
            # loop.exec_()

            # TODO: Add signal for error cases


    def download_finished(self):
        """
        """
        reply = self.sender()
        if reply.error():
            print("Download failed. Error string:\n", reply.errorString())
        print("Download finished! Reply:", reply)
        file_info = QFileInfo(reply.url().path())
        file_name = file_info.fileName()
        file_path = self.current_path + '/' + file_name
        out_file = QFile(file_path)
        print("Path:", file_path)
        if QFile.exists(file_name):
            print("File exists")
            # TODO: Add better notification
            out_file = QFile(file_name)
        if not out_file.open(QIODevice.WriteOnly):
            out_file = None
            print("Failed to open file")
            # TODO: Add better notification

        out_file.write(reply.readAll())
        reply.deleteLater()



        # self.replies.remove(reply)






app = QApplication(sys.argv)
window = MyApp()
window.show()

sys.exit(app.exec_())
