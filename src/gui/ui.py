# -*- coding=utf-8 -*-
"""
Defines main UI dialog.
"""

# own #
from gui.params import *
from pref.opt import __version__

# external #
from PyQt4.QtGui import QWidget, QVBoxLayout, QGridLayout,\
                        QGroupBox, QLabel, QPushButton, QApplication
#from PyQt4.QtCore import Qt

class GUI(QWidget):

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.layout = QVBoxLayout()

        self.kanjiGroup = QGroupBox('Kanji')
        self.kanjiLayout = QGridLayout()

        self.day = QLabel()
        self.month = QLabel()
        self.week = QLabel()
        self.year = QLabel()
        self.kanjiLayout.addWidget(self.day, 0, 0)
        self.kanjiLayout.addWidget(self.month, 0, 1)
        self.kanjiLayout.addWidget(self.week, 1, 0)
        self.kanjiLayout.addWidget(self.year, 1, 1)
        self.kanjiGroup.setLayout(self.kanjiLayout)

        self.getAll = QPushButton('Get all')
        self.layout.addWidget(self.getAll)

        self.setLayout(self.layout)

        self.init_composition()
        self.init_contents()
        self.init_actions()

    def init_composition(self):
        self.setWindowTitle(NAME + ' ' + __version__)
        desktop = QApplication.desktop()
        self.setGeometry((desktop.width() - WIDTH)/2, (desktop.height() - HEIGHT)/2, WIDTH, HEIGHT)

    def init_contents(self):
        pass

    def init_actions(self):
        pass
