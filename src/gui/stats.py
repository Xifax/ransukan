# -*- coding=utf-8 -*-
"""
Kanji selection statistics UI dialog.
"""
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QGridLayout, QPushButton, QLabel

class StatsUI(QWidget):
    def __init__(self, parent=None):
        super(StatsUI, self).__init__(parent)

        self.layout = QGridLayout()

        self.statPlot = QLabel("Here be matplotlib widget, Y: picked | X: frequency (least to most)")
        self.refreshPlot = QPushButton('&Refresh')
        self.runTest = QPushButton('&Test')
        self.clearStats = QPushButton('&Clear')
        self.switchFreqDom = QPushButton('&Switch')

        self.layout.addWidget(self.statPlot, 0, 0, 1, 4)
        self.layout.addWidget(self.refreshPlot, 1, 0)
        self.layout.addWidget(self.runTest, 1, 1)
        self.layout.addWidget(self.clearStats, 1, 2)
        self.layout.addWidget(self.switchFreqDom, 1, 3)

        self.setLayout(self.layout)
        self.setWindowTitle('Stats')
        self.setWindowFlags(Qt.Tool)
