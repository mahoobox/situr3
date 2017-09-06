#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      websnapshot.py
#
#      Copyright 2014 Recursos Python - www.recursospython.com
#
#

import sys

from PyQt4.QtCore import QUrl
from PyQt4.QtGui import (QApplication, QHBoxLayout, QMainWindow,
                         QPixmap, QWidget)
from PyQt4.QtWebKit import QWebView


class Widgets(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Simple Web Browser")
        self.widget = QWidget(self)
        self.webview = QWebView()
        self.webview.load(QUrl("http://www.situr.boyaca.gov.co/"))
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.webview)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
        self.webview.page().mainFrame().loadFinished.connect(
            self.load_finished)
    
    def load_finished(self):
        self.snapshot()
    
    def snapshot(self):
        pageview = self.webview.page().view()
        pixmap = QPixmap(pageview.size())
        pageview.render(pixmap)
        pixmap.save("output.png")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Widgets()
    window.show()
    sys.exit(app.exec_())