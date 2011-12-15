# -*- coding=utf-8 -*-
"""
Defines main UI dialog.
"""

# own #
from gui.params import *
from pref.opt import __version__
from alg.altogether import algs, random_int
from db.kanji import Kanji

# external #
from PyQt4.QtGui import QWidget, QGridLayout, \
                        QGroupBox, QLabel, QPushButton, QApplication, QFont, \
                        QComboBox

from PyQt4.QtCore import Qt

class GUI(QWidget):

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        #self.layout = QVBoxLayout()
        self.layout = QGridLayout()

        self.kanjiGroup = QGroupBox('Kanji by day, week, month, year')
        self.kanjiLayout = QGridLayout()

        # Kanji ui group
        self.day = QLabel(KANJI)
        self.week = QLabel(KANJI)
        self.month = QLabel(KANJI)
        self.year = QLabel(KANJI)

        self.dayLabel = QLabel('Day')
        self.weekLabel = QLabel('Week')
        self.monthLabel = QLabel('Month')
        self.yearLabel = QLabel('Year')

        self.kanjiLayout.addWidget(self.day, 0, 0)
        self.kanjiLayout.addWidget(self.week, 0, 1)
        self.kanjiLayout.addWidget(self.dayLabel, 1, 0)
        self.kanjiLayout.addWidget(self.weekLabel, 1, 1)

        self.kanjiLayout.addWidget(self.month, 2, 0)
        self.kanjiLayout.addWidget(self.year, 2, 1)
        self.kanjiLayout.addWidget(self.monthLabel, 3, 0)
        self.kanjiLayout.addWidget(self.yearLabel, 3, 1)

        self.kanjiGroup.setLayout(self.kanjiLayout)

        # Main layout
        self.getAll = QPushButton('Get all')
        self.showStats = QPushButton('Stats')
        self.quitApp = QPushButton('Quit')
        self.methodCombo = QComboBox()
        self.layout.addWidget(self.kanjiGroup, 0, 0, 1, 2)
        self.layout.addWidget(self.getAll, 1, 0)
        self.layout.addWidget(self.showStats, 1, 1)
        self.layout.addWidget(self.methodCombo, 2, 0, 1, 2)
        self.layout.addWidget(self.quitApp, 3, 0, 1, 2)

        self.setLayout(self.layout)

        self.init_composition()
        self.init_contents()
        self.init_actions()

    def init_composition(self):
        self.setWindowTitle(NAME + ' ' + __version__)
        desktop = QApplication.desktop()
        self.setGeometry((desktop.width() - WIDTH)/2, \
                        (desktop.height() - HEIGHT)/2, WIDTH, HEIGHT)

    def init_contents(self):
        self.kanjiGroup.setAlignment(Qt.AlignCenter)

        self.day.setAlignment(Qt.AlignCenter)
        self.week.setAlignment(Qt.AlignCenter)
        self.month.setAlignment(Qt.AlignCenter)
        self.year.setAlignment(Qt.AlignCenter)

        self.dayLabel.setAlignment(Qt.AlignCenter)
        self.weekLabel.setAlignment(Qt.AlignCenter)
        self.monthLabel.setAlignment(Qt.AlignCenter)
        self.yearLabel.setAlignment(Qt.AlignCenter)

        self.day.setFont(QFont(PRETTY_FONT, KANJI_SIZE))
        self.week.setFont(QFont(PRETTY_FONT, KANJI_SIZE))
        self.month.setFont(QFont(PRETTY_FONT, KANJI_SIZE))
        self.year.setFont(QFont(PRETTY_FONT, KANJI_SIZE))

        self.methodCombo.addItems(algs.keys())
        self.methodCombo.setCurrentIndex(0)

    def init_actions(self):
        self.quitApp.clicked.connect(self.close)
        self.getAll.clicked.connect(self.get_all)

    def get_all(self):
        kanji_set = []
        while(len(kanji_set) != 4):
            #integer = random_int(str(self.methodCombo.currentText()))
            #print integer
            #kanji = Kanji.get_random(integer)
            kanji = Kanji.get_random(random_int(str(self.methodCombo.currentText())))
            if kanji is not None:
                kanji_set.append(kanji.character)
        self.day.setText(kanji_set.pop())
        self.week.setText(kanji_set.pop())
        self.month.setText(kanji_set.pop())
        self.year.setText(kanji_set.pop())

    def pretty_font(self):
        pass
