# -*- coding=utf-8 -*-
"""
Kanji selection statistics UI dialog.
"""
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QGridLayout, QPushButton, QLabel

#from graphWidget import MplWidget

class StatsUI(QWidget):
    def __init__(self, parent=None):
        super(StatsUI, self).__init__(parent)

        self.create_ui_components()
        self.compose_ui()
        self.init_composition()
        self.init_components()
        self.init_actions()

    def create_ui_components(self):
        self.layout = QGridLayout()

        self.statPlot = QLabel("Here be matplotlib widget, Y: picked | X: frequency (least to most)")
        #self.statPlot = MplWidget()
        self.refreshPlot, self.runTest, self.clearStats, self.switchFreqDom = \
        QPushButton('&Refresh'), QPushButton('&Test'), QPushButton('&Clear'), QPushButton('&Switch')

    def compose_ui(self):
        self.layout.addWidget(self.statPlot, 0, 0, 1, 4)
        self.layout.addWidget(self.refreshPlot, 1, 0)
        self.layout.addWidget(self.runTest, 1, 1)
        self.layout.addWidget(self.clearStats, 1, 2)
        self.layout.addWidget(self.switchFreqDom, 1, 3)

        self.setLayout(self.layout)

    def init_composition(self):
        self.setWindowTitle('Stats')
        self.setWindowFlags(Qt.Tool)

    def init_components(self):
        self.refreshPlot.setToolTip('Update plot based on db stats')
        self.runTest.setToolTip('Run automated selection/distribution batch-tests')
        self.clearStats.setToolTip('Reset currently accumulated distribution stats')
        self.switchFreqDom.setToolTip('Switch plot between displaying \
n_picked(frequency) or n_picked(dominance)')

    def init_actions(self):
        pass

    ##### actions #####
